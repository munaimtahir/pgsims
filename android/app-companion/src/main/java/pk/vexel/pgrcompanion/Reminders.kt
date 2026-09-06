package pk.vexel.pgrcompanion

import android.app.AlarmManager
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Date
import java.util.Locale
import java.util.TimeZone

/**
 * Personal Workspace reminders. Entirely local: nothing here contacts a network, and nothing here
 * has any institutional dependency. The declared POST_NOTIFICATIONS permission exists for this
 * and only this.
 */
object Reminders {

    const val CHANNEL_ID = "reminders"
    const val ACTION_FIRE = "pk.vexel.pgrcompanion.REMINDER"
    const val EXTRA_ID = "reminder_id"
    const val EXTRA_TITLE = "reminder_title"

    /** Reminders are day-granular, so they are delivered at a civil hour rather than at midnight. */
    const val REMINDER_HOUR = 9

    private const val DISPLAY_PATTERN = "dd MMM yyyy"

    /**
     * Material's date picker reports the selection as UTC midnight. Translate that calendar day into
     * [REMINDER_HOUR] in the device's own time zone, so a reminder set for the 12th fires on the
     * 12th regardless of the user's offset.
     */
    fun triggerAtFor(utcMidnightMillis: Long, zone: TimeZone = TimeZone.getDefault()): Long {
        val utc = Calendar.getInstance(TimeZone.getTimeZone("UTC")).apply { timeInMillis = utcMidnightMillis }
        return Calendar.getInstance(zone).apply {
            clear()
            set(utc.get(Calendar.YEAR), utc.get(Calendar.MONTH), utc.get(Calendar.DAY_OF_MONTH), REMINDER_HOUR, 0, 0)
        }.timeInMillis
    }

    fun formatDueDate(triggerAtMillis: Long, zone: TimeZone = TimeZone.getDefault()): String =
        SimpleDateFormat(DISPLAY_PATTERN, Locale.getDefault())
            .apply { timeZone = zone }
            .format(Date(triggerAtMillis))

    /** A reminder is worth an alarm only while it is unfinished, dated and still ahead of us. */
    fun isSchedulable(reminder: ReminderRecord, now: Long): Boolean =
        !reminder.completed && (reminder.dueAtMillis ?: 0L) > now

    /** minSdk is 26, so the channel always exists — there is no pre-O path to guard. */
    fun createChannel(context: Context) {
        val manager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        manager.createNotificationChannel(
            NotificationChannel(CHANNEL_ID, "Residency reminders", NotificationManager.IMPORTANCE_DEFAULT).apply {
                description = "Due dates you added to PGR Companion."
            }
        )
    }

    fun schedule(context: Context, reminder: ReminderRecord, now: Long = System.currentTimeMillis()) {
        if (!isSchedulable(reminder, now)) return
        val alarms = context.getSystemService(Context.ALARM_SERVICE) as? AlarmManager ?: return
        // Inexact and idle-tolerant: correct for a day-granular reminder and, unlike an exact alarm,
        // it needs no additional permission and no special-access prompt.
        runCatching {
            alarms.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, reminder.dueAtMillis!!, pendingIntent(context, reminder))
        }
    }

    fun cancel(context: Context, reminder: ReminderRecord) {
        val alarms = context.getSystemService(Context.ALARM_SERVICE) as? AlarmManager ?: return
        runCatching { alarms.cancel(pendingIntent(context, reminder)) }
    }

    /** Re-arms everything still in the future. Used after a reboot, when alarms are dropped. */
    fun rescheduleAll(context: Context, reminders: List<ReminderRecord>, now: Long = System.currentTimeMillis()) {
        reminders.forEach { schedule(context, it, now) }
    }

    private fun pendingIntent(context: Context, reminder: ReminderRecord): PendingIntent {
        val intent = Intent(context, ReminderReceiver::class.java).apply {
            action = ACTION_FIRE
            // The id is part of the *data*, not just the extras: extras are ignored when
            // PendingIntent equality is computed, so without it every reminder would collide.
            data = android.net.Uri.parse("pgrcompanion://reminder/${reminder.id}")
            putExtra(EXTRA_ID, reminder.id)
            putExtra(EXTRA_TITLE, reminder.title)
        }
        return PendingIntent.getBroadcast(
            context,
            0,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE,
        )
    }

    fun notify(context: Context, id: String, title: String) {
        if (!NotificationManagerCompat.from(context).areNotificationsEnabled()) return
        val open = PendingIntent.getActivity(
            context,
            0,
            Intent(context, MainActivity::class.java).addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP),
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE,
        )
        val notification = NotificationCompat.Builder(context, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_launcher_foreground)
            .setContentTitle("Residency reminder")
            .setContentText(title)
            .setAutoCancel(true)
            .setContentIntent(open)
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)
            .build()
        // Permission can be revoked between scheduling and delivery; that is a no-op, not a crash.
        runCatching { NotificationManagerCompat.from(context).notify(id.hashCode(), notification) }
    }
}

/**
 * Delivers a due reminder, and re-arms surviving reminders after a reboot. Not exported: it handles
 * one protected system broadcast and one alarm this app scheduled for itself.
 */
class ReminderReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        when (intent.action) {
            Intent.ACTION_BOOT_COMPLETED, Intent.ACTION_MY_PACKAGE_REPLACED -> {
                Reminders.createChannel(context)
                Reminders.rescheduleAll(context, LocalStore(context).read().reminders)
            }
            Reminders.ACTION_FIRE -> {
                val id = intent.getStringExtra(Reminders.EXTRA_ID) ?: return
                val title = intent.getStringExtra(Reminders.EXTRA_TITLE).orEmpty().ifBlank { "You have a reminder due." }
                Reminders.createChannel(context)
                Reminders.notify(context, id, title)
            }
        }
    }
}
