# Configuration

SMAT allows the user to configure some aspects of its execution. This can be done by editing the [nimrod/tests/env-config.json](nimrod/tests/env-config.json) file. This session will discuss the available options for customization.

## General
### java_home
By default, SMAT will use the `JAVA_HOME` env var to populate Java Home. However, it's possible to override this value by setting the `java_home` property in the configuration file.