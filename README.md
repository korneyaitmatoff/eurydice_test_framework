# Test framework
This is solution for fast build test framework

__Steps for start__:

Build project:\
```eurydice project init --project-name [PROJECT_NAME]```

Add service:\
```eurydice service add --project-name [PROJECT_NAME] --service-name [SERVICE_NAME]```

If you use database in your tests, you can build pgsql database locally with using docker-compose:
```eurydice database init --user [USER] --password [PASSWORD] --database [DATABASE]```

Now eurydice supports only pgsql.

Now project in beta. You can suggest the features.

