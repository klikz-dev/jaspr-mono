This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Setting environment

Copy the .env.example file to .env and update the environment to the appropriate value. Expo/React Native do not have access to environment variables in process.env, the build tools do however. The build tools copy the environment variables into src/config.native.js via the app.config.js file. The web version does have access to environment variables which are loaded into src/config.js at runtime. This way, environment variables can be consumed in the application by importing the config file so consuming them does not require different code paths for web or native.

| Variable              | Value                                      | Purpose                         | Notes                                                                                                                                                                             |
| --------------------- | ------------------------------------------ | ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| REACT_APP_VERSION     | \$npm_package_version                      | Specifies release version       | This value should not be changed. It automatically pulls the release version from the package.json file. It is primarily used to indicate to sentry the build application version |
| REACT_APP_ENVIRONMENT | "production" or "staging", etc             | Indicates the environment       | This is primarily used by sentry to indicate whcih environment, such as staging or integration where an error was encountered                                                     |
| REACT_APP_SENTRY_DSN  | Sentry DSN URL                             | Jaspr's Sentry provided DSN URL | This routes errors to our project in Sentry                                                                                                                                       |
| REACT_APP_API_ROOT    | https://staging01-api.willow.technology/v1 | The base url for APi requests   |                                                                                                                                                                                   |

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.<br>
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.<br>
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.<br>
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.<br>
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.<br>
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (Webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: https://facebook.github.io/create-react-app/docs/code-splitting

### Analyzing the Bundle Size

This section has moved here: https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size

### Making a Progressive Web App

This section has moved here: https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app

### Advanced Configuration

This section has moved here: https://facebook.github.io/create-react-app/docs/advanced-configuration

### Deployment

This section has moved here: https://facebook.github.io/create-react-app/docs/deployment

### `npm run build` fails to minify

This section has moved here: https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify
