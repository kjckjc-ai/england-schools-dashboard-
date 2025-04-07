# England Schools Dashboard - Streamlit Deployment

This file contains instructions for deploying the England Schools Dashboard to Streamlit Community Cloud.

## Deployment Steps

1. Create a GitHub repository:
   - Create a new repository on GitHub
   - Push the contents of this directory to the repository

2. Deploy to Streamlit Community Cloud:
   - Go to https://streamlit.io/cloud
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository and branch
   - Set the main file path to "app.py"
   - Click "Deploy"

That's it! Your dashboard will be deployed and accessible via a public URL.

## Important Notes

- The free tier of Streamlit Community Cloud includes:
  - Public access to your app
  - Automatic updates when you push changes to your repository
  - Sharing capabilities

- For the best experience:
  - Keep your database file in the repository (it will be included in the deployment)
  - Any data updates will require pushing changes to the repository

## Maintenance

To update the deployed application:
1. Make changes to your local files
2. Push the changes to your GitHub repository
3. Streamlit Community Cloud will automatically update your app

## Local Development

To run the dashboard locally:
```
streamlit run app.py
```

This will start the Streamlit server and open the dashboard in your web browser.
