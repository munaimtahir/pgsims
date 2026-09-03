# Repository cleanup

The old `fmu.pg.sims` Android source, authentication screens, Retrofit/OkHttp client, FMU logo, network security configuration, and FMU Android tests were removed from the active app source boundary. The new app uses `pk.vexel.pgrcompanion` and `PGR Companion` strings only. Existing top-level historical/project material outside the Android module was not mass-deleted; unrelated user files remain untouched.

The original institutional signing setup was not modified. Release signing remains owner-controlled through `fmuSigningPropertiesFile` and no secrets are committed.
