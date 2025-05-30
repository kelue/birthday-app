# Birthday Web App

#### Video Demo: https://youtu.be/ks7KEw0bDn8

#### Description: 

The web application, "Birthday App" allows users to create a custom link to send to their friends and family. When someone clicks on the link, they can enter their name and a personalized message for the birthday person. The birthday person will then receive all of the messages in one place, creating a special and unique birthday celebration. To use the app, users simply need to sign up and create a profile. 

From there, they can create a new link for the birthday celebration. They can customize the link with pictures to be displayed on the pages. Once the link is created, the user can share it with their friends and family via email, social media, or any other means. When someone clicks on the link, they will be directed to a page where they can enter their name and message. The birthday person will be able to view all of the messages in one place, creating a heartfelt and memorable birthday celebration. 

With "Birthday App" it's easy to make every birthday celebration special and unique. Give it a try and bring a smile to the face of someone you love! 

### Tooling

- The web application, "Birthday App" is built using Flask, a popular Python web framework, and Bootstrap 5, a front-end framework for designing responsive and mobile-first websites. 
- I use a PostgreSQL database instance to store user profile settings and birthday messages.
- This a simple project and there are some limitations such as those listed below and feature upgrades which can be added in time.
- Vist the live Birthday App [here](https://birthday-app.onrender.com) or you can set up your own local instance and run the server locally. You need to ensure that you have python & pip installed localled to be able to run flask.
- You also ned to setup a postgresql database instance and connect it to the app using environmental variables. You can also connect a different database software but you may need to refactor the sql statement to enable it work.

#### Local Setup
1. clone the repo
2. configure a database preferrably postgresql database instance on your system
2. Use the `birthday.sql` to setup yout postgres database tables or you can edit the sql prompts in order to use another database
3. Create a `.env` file . See the env.example file for reference
4. Run the app on your local server

#### Current Limitations of the project
- user cannot edit profile
- user cannot change only one image, all three must be changed for the form to submit
- user cannot delete account
