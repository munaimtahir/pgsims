package pk.vexel.pgrcompanion

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test
import java.util.Calendar
import java.util.TimeZone

/**
 * The scheduling arithmetic, isolated from AlarmManager. The bug this guards against is a reminder
 * for the 12th firing on the 11th for anyone east or west of UTC.
 */
class RemindersTest {

    private fun fieldsOf(millis: Long, zone: TimeZone): Triple<Int, Int, Int> {
        val calendar = Calendar.getInstance(zone).apply { timeInMillis = millis }
        return Triple(calendar.get(Calendar.DAY_OF_MONTH), calendar.get(Calendar.HOUR_OF_DAY), calendar.get(Calendar.MINUTE))
    }

    /** Material's date picker reports UTC midnight for the chosen calendar day. */
    private fun utcMidnight(year: Int, monthZeroBased: Int, day: Int): Long =
        Calendar.getInstance(TimeZone.getTimeZone("UTC")).apply {
            clear(); set(year, monthZeroBased, day, 0, 0, 0)
        }.timeInMillis

    @Test fun `a chosen day fires on that same day at the reminder hour, in Karachi`() {
        val zone = TimeZone.getTimeZone("Asia/Karachi") // UTC+5, where this product's users are
        val trigger = Reminders.triggerAtFor(utcMidnight(2026, Calendar.SEPTEMBER, 12), zone)
        assertEquals(Triple(12, Reminders.REMINDER_HOUR, 0), fieldsOf(trigger, zone))
    }

    @Test fun `the same holds west of UTC, where a naive offset would slip a day`() {
        val zone = TimeZone.getTimeZone("America/Los_Angeles")
        val trigger = Reminders.triggerAtFor(utcMidnight(2026, Calendar.SEPTEMBER, 12), zone)
        assertEquals(Triple(12, Reminders.REMINDER_HOUR, 0), fieldsOf(trigger, zone))
    }

    @Test fun `the formatted due date matches the day that will actually fire`() {
        val zone = TimeZone.getTimeZone("Asia/Karachi")
        val trigger = Reminders.triggerAtFor(utcMidnight(2026, Calendar.SEPTEMBER, 12), zone)
        assertEquals("12 Sep 2026", Reminders.formatDueDate(trigger, zone))
    }

    @Test fun `only unfinished, dated, future reminders are worth an alarm`() {
        val now = 1_000_000L
        assertTrue(Reminders.isSchedulable(ReminderRecord(title = "t", dueDate = "", dueAtMillis = now + 1), now))
        assertFalse(Reminders.isSchedulable(ReminderRecord(title = "t", dueDate = "", dueAtMillis = now - 1), now))
        assertFalse(Reminders.isSchedulable(ReminderRecord(title = "t", dueDate = "", dueAtMillis = null), now))
        assertFalse(
            Reminders.isSchedulable(
                ReminderRecord(title = "t", dueDate = "", completed = true, dueAtMillis = now + 1),
                now,
            )
        )
    }
}
