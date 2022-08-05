# MHS Updates

Disclaimer: not all features are currently available. Please continue to check back for updates.

Getting the latest information from Mayfield City Schools can be a real pain sometimes. This is a program designed for and maintained by Mayfield High School students to help solve that problem. MHS Updates takes news from official sources, and sends it to places where students will see it. It also allows students to submit pieces of news that were not announced digitally, which will then be reviewed by a team of moderators. Important updates that apply to everyone will be pushed to an "important" channel by moderators. This way members can turn off updates from specific sources without missing important news.

## Self-hosting

To start, copy all of the sample files to the root directory and modify them. Create a folder named 'logos' within the static/img folder and create a subdirectory for each integration you use (ex. "rss", "twitter", etc.). Place the icons (in png format) inside their respective folders (ex. "/static/img/rss/name_of_connection.png"). Then you will need to set up an N8N instance and import the n8n_sample_profile.json file and modify it. Set up a Google Form which exports to a Google Sheet, and use that same Google account to access the Google Sheets API. Then you can connect it with N8N. This system is in place to ensure that people who sign up are a part of Mayfield City Schools and also to allow account management through this service independent of Google once users have completed the initial sign-up process.

## API Reference

MHS Updates API v1 developer notes:

  + Remember, all routes must return something 
    for Flask to forward to the client.

  + All routes must be added to VALID_ROUTES

  + Format for API methods:
    `def method(self, request, *args)`

jvadair 2022

---

#### I'm a little teapot

```http
  POST /api/v1/Tea
```

#### Update user credentials

```http
  POST /api/v1/SetCredentials
```

| Header        |  Description                                                                       |
| :------------ | :--------------------------------------------------------------------------------- |
| `X-API-Key`   | **Required**. API key as specified in the config.json file. SHOULD BE VERY SECURE! |

**Received data format:**

JSON, List of lists, whose indexes are:

    0: Timestamp
    1: Email Address
    2: Password

Also see n8n_sample_profile.json
#### Login

```http
  POST /api/v1/Login
```

| Parameter    | Type     | Description                       |
| :----------- | :------- | :-------------------------------- |
| `email`      | `string` | **Required**. User's email        |
| `password`   | `string` | **Required**. User's password     |

#### SetPreferences

```http
  POST /api/v1/SetPreferences
```

| Parameter    | Type     | Description                                                                              |
| :----------- | :------- | :--------------------------------------------------------------------------------------- |
| `*`          | `string` | **Required**. Preference to set.  (Can set multiple by sending multiple parameters)      |

#### ChangePassword

```http
  POST /api/v1/Login
```

| Parameter           | Type     | Description                        |
| :------------------ | :------- | :--------------------------------- |
| `old_password`      | `string` | **Required**. The old password     |
| `new_password`      | `string` | **Required**. The new password     |

#### Logout

```http
  POST /api/v1/Logout
```

## Authors

- [@jvadair](https://www.gitlab.com/jvadair)


## Documentation
Not yet available


## Contributing

Contributions are always welcome!

Contact [dev@jvadair.com](mailto:dev@jvadair.com) if you would like to help.


## License

[MIT](https://choosealicense.com/licenses/mit/)

```
MIT License

Copyright (c) 2022 James Adair

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
## Roadmap
A private (due to technical limitations) roadmap is available on Nexus, contact [dev@jvadair.com](mailto:dev@jvadair.com) for more info.

