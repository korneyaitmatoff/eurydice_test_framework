# Test framework
This is solution for fast build test framework

__Steps for start__:

Build project:\
```eurydice project init --project-name [PROJECT_NAME] --login [LOGIN] --password [PASSWORD]```

login and password for tests database.

Add service:\
```eurydice service add --project-name [PROJECT_NAME] --service-name [SERVICE_NAME]```

Run tests:\
```eurydice tests run --mark [MARK]```
Use mark "all" for run all tests.


Now eurydice supports only pgsql.

Now project in beta. You can suggest the features.

