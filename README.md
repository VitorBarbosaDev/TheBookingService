# The Booking Service

![image](https://github.com/VitorBarbosaDev/TheBookingService/assets/46977318/9ac3f0b8-d643-4f19-b1dd-650ffde0e9c5)

TheBookingService** is a cutting-edge, web-based platform designed to transform the way clients and service providers connect and manage appointments. This platform stands out by providing a user-friendly interface, comprehensive management tools, and a seamless booking process, making it easier than ever to book a wide range of services online.

Live Site: [View Live Site](https://thebookingservice-3eba3aca87b4.herokuapp.com/)
Repo: [GitHub Repository](https://github.com/VitorBarbosaDev/TheBookingService)

### Why Choose TheBookingService?
- **Efficiency at Your Fingertips**: Quick booking, rescheduling, and cancellation of services.
- **Comprehensive Service Management**: Service providers can easily manage their services, schedules, and client interactions.
- **Secure and Reliable**: Integrated with Stripe for secure payments and robust data handling with PostgreSQL.


---

## Table of Contents

- [User Experience (UX)](#user-experience-ux)
- [Design](#design)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Deployment](#deployment)
- [Testing](#testing)
- [Credits](#credits)

---

## User Experience (UX)

### Goals

#### Target Audience
- **Individuals looking to book services**: From beauty services to home repairs, users can find and book a variety of services online.
- **Service Providers**: Offering a platform for service providers to manage appointments, promote services, and connect with clients.
- **Busy Professionals and Households**: For anyone seeking a convenient way to manage appointments without the hassle of traditional booking methods.


#### User Stories

##### New User Goals
- As a new user, I want to easily navigate the website so that I can find services without hassle.
- As a new user, I want to quickly register so I can start booking services immediately.
- As a new user, I want to explore various services offered so that I can choose what best fits my needs.

##### Returning User Goals
- As a returning user, I want to view and manage my upcoming and past bookings easily from my profile to stay organized.
- As a returning user, I want to receive updates on any changes to my bookings or new offers so that I am always informed.
- As a returning user, I want to be able to rate and review services I have used to inform others of my experience.

##### Frequent User Goals
- As a frequent user, I want the system to recommend services based on my previous bookings to enhance my experience.
- As a frequent user, I would like to receive loyalty benefits or discounts as I continue to use the service regularly.

##### Service Provider Goals
- As a service provider, I want access to a dashboard where I can see an overview of my business performance on the platform.
- As a service provider, I want to manage bookings made by users, including accepting, rescheduling, or cancelling bookings efficiently.
- As a service provider, I want to create and manage promotions or discounts for my services to attract more customers.

##### Admin Goals
- As an admin, I need to moderate reviews and feedback to ensure authenticity and appropriateness of the content.
- As an admin, I want to view analytics on user behavior and service performance to make data-driven decisions for the platform.


### Design

#### Overview
The design of TheBookingService prioritizes clarity, ease of use, and responsiveness, ensuring a seamless experience across all devices. With a professional color palette, intuitive layout, and accessible typography, the platform invites users of all tech-savviness levels to easily navigate and manage their bookings.

#### Colour Scheme
- **Neutral Palette**: Utilizes a soothing combination of greys and whites, providing a clean and uncluttered background that highlights content and features effectively.
- **Accent Colors**: Strategic use of blue accents not only adds visual interest but also serves as a guide through the interactive elements of the site, enhancing user navigation and accessibility.

#### Typography
- **Main Font**: Lato is used throughout the platform for its modern appearance and excellent readability. It helps keep text clear and legible at various sizes, which is crucial for usability.
- **Consistent Usage**: Typography is kept consistent with the bootstrap framework integration, ensuring that the textual content is both aesthetically pleasing and functionally scalable across different devices and resolutions.

#### Imagery
- **Purposeful Imagery**: High-quality images are used not just for aesthetics but to convey professionalism and build trust. They are carefully chosen to reflect the diverse range of services available through the platform.
- **Iconography**: FontAwesome icons are integrated throughout the user interface to support text labels and improve visual communication of features and actions.

#### Responsive Design
- **Fluid Layouts**: Built on Bootstrap 5, the site employs fluid grid layouts that adapt to the screen sizes of various devices, from mobile phones to large desktops.
- **Adaptive Components**: Interactive elements like forms, buttons, and navigation menus are designed to be touch-friendly and easy to use on mobile devices.
- **Media Queries**: Extensive use of CSS media queries ensures that the site's layout, typography, and components adjust gracefully to different window sizes and orientations.

#### User Interface (UI) Enhancements
- **Navigation**: The top navigation bar is fixed and responsive, adjusting to user's device and screen size, ensuring that navigation options are always accessible without overcrowding the screen.
- **Forms and Buttons**: Forms are styled with Crispy Forms & Crispy Bootstrap5, which provide a polished look and feel. Buttons are designed to be eye-catching and consistent across the platform, making them easy to locate and use.
- **Toasts and Modals**: Utilized to provide immediate feedback or important notifications without navigating away from the current page, enhancing the interactivity and responsiveness of the user experience.

#### Accessibility
- **A11y Practices**: Adheres to accessibility best practices, ensuring that the website is usable by people with disabilities. This includes sufficient contrast ratios for text and background colors.
- **ARIA Labels**: Where necessary, ARIA labels are applied to icons and non-text elements to enhance screen reader support.


---

## Features

### Existing Features
- **User Profiles**: Comprehensive management for user profiles, with separate distinctions between business and personal accounts.
- **Service Management**: Service providers can list, update, and remove their offerings, with rich descriptions and categorization.
- **Booking System**: Robust booking functionality, including viewing past and upcoming bookings for users and managing received bookings for providers.
- **Payment System**: Integrated Stripe payments allow for secure booking confirmations and cancellations, including refund capabilities.
- **Reviews and Ratings**: Users can review and rate services after completion, influencing the service visibility and provider credibility.
- **Dynamic Scheduling and Booking**: Automatic slot generation based on business hours and real-time availability.
- **Search Functionality**: Users can search for services or businesses directly, with keyword filtering.

### Planned Features
- **Advanced Filtering**: Introducing more granular filters for users to find services by date, type, or rating.
- **Provider Dashboard**: A dashboard for providers to get insights into their service performance, booking trends, and customer demographics.
- **Real-Time Updates**: Implementing WebSocket technology to provide users and providers with real-time updates on booking changes.
- **Customer Support Chat**: A built-in chat system to assist users with bookings and inquiries promptly.
- **Promotional Discounts**: Tools for providers to offer promotional rates and discounts on their services.
- **Enhanced Mobile Experience**: Optimizations to improve accessibility and usability on mobile devices.
- **Accessibility Enhancements**: Upgrades to make the site more accessible to individuals with disabilities.


---

## Technologies Used

### Languages
- **HTML5**
- **CSS3**
- **JavaScript**
- **Python**

### Frameworks & Libraries
- **Django**: Main back-end framework.
- **Bootstrap 5**: Front-end framework for layout and design.
- **jQuery**: JavaScript library used for handling dynamic content.
- **Stripe**: Integrated for payment processing.

### Tools & Services
- **Git**: Version control system.
- **GitHub**: Online platform to host and review code.
- **Heroku**: Cloud platform as a service used to deploy the web application.
- **PostgreSQL**: Primary database solution.
- **Cloudinary**: Used for image uploads and serving them on the platform.
- **WhiteNoise**: Manages static files efficiently.
- **django-allauth**: Provides authentication mechanisms.
- **Crispy Forms & Crispy Bootstrap5**: Used for styling Django forms.

### Others
- **dotenv**: Utilized for managing environment variables securely.


---

## Deployment & Local Development

### Deployment to Heroku with PostgreSQL and Cloudinary

This Django application is configured to be hosted on Heroku, using PostgreSQL for the database and Cloudinary for image storage. Follow these steps to deploy:

#### Heroku Deployment

1. **Create a Heroku account:** If you don't have one, sign up at [Heroku](https://www.heroku.com/).
2. **Install Heroku CLI:** Follow the instructions [here](https://devcenter.heroku.com/articles/heroku-cli) to install the Heroku Command Line Interface.
3. **Login to Heroku:** Run `heroku login` in your terminal and log in through the browser.
4. **Create a new Heroku app:** In your terminal, run `heroku create your-app-name`.
5. **Set up ElephantSQL:** 
   - Sign up at [ElephantSQL](https://www.elephantsql.com/).
   - Create a new instance and choose the appropriate plan.
   - Copy the URL provided by ElephantSQL.
   - Set the `DATABASE_URL` in Heroku's settings to this URL.  
6. **Set up Stripe:**
   - Sign up or log in at [Stripe](https://stripe.com/).
   - Navigate to the API keys section under the Developers tab.
   - Copy your `STRIPE_PUBLIC_KEY` and `STRIPE_SECRET_KEY`.
   - Add these keys to your Heroku app's environment variables.
7. **Set up environment variables:** Configure your environment variables in Heroku under the app's "Settings" tab. You'll need to set variables like  `SECRET_KEY`, `DATABASE_URL`,`CLOUDINARY_URL`,`STRIPE_PUBLIC_KEY`,`STRIPE_SECRET_KEY`,`STRIPE_WH_SECRET`,`EMAIL_HOST_PASS`,`EMAIL_HOST_USER`
8. **Deploy the app:** Push your code to Heroku using Git (`git push heroku main`).
9. **Run migrations:** After deployment, run `heroku run python manage.py migrate` to apply database migrations.
10. **Open your app:** You can now access your app by running `heroku open` or visiting the app's URL.

#### Cloudinary Setup

1. **Create a Cloudinary account:** Sign up at [Cloudinary](https://cloudinary.com/).
2. **Get your Cloudinary URL:** Navigate to the "Dashboard" to find your Cloudinary URL.
3. **Set the Cloudinary URL in Heroku:** Add your Cloudinary URL to the environment variables in your Heroku app settings.

### Local Development

#### Cloning the Repository

1. **Open the Terminal:** On your local machine, open the terminal.
2. **Clone the Repository:** Run `git clone https://github.com/VitorBarbosaDev/TheBookingService/.git` to clone the forked repository.
3. **Navigate to the Directory:** Enter the cloned directory (`cd TheBookingService`).
4. **Install Dependencies:** Run `pip install -r requirements.txt` to install required Python packages.
5. **Create a .env file:** Set up a `.env` file with necessary environment variables like `SECRET_KEY`, `DATABASE_URL`,`CLOUDINARY_URL`,`STRIPE_PUBLIC_KEY`,`STRIPE_SECRET_KEY`,`STRIPE_WH_SECRET`,`EMAIL_HOST_PASS`,`EMAIL_HOST_USER`,`DEVELOPMENT`.
6. **Run Migrations:** Execute `python manage.py migrate` to apply database migrations.
7. **Start the Development Server:** Run `python manage.py runserver` to start the Django development server.
8. **Open the Application:** Open `localhost:8000` in your web browser to view the application.

This comprehensive guide ensures that TheBookingService is set up with a solid foundation for both production and development environments, incorporating robust services like Heroku for hosting, ElephantSQL for database management, Cloudinary for image storage, and Stripe for secure payment processing, thus ensuring scalability and operational efficiency.

---

## Testing

Testing information can be found in the detailed [Testing.md](https://github.com/yourUsername/TheBookingService/blob/main/TESTING.md) document.

---

## Credits

### Content
- The text for the site was provided by the project owner.

### Media
- All images were sourced or created by the project owner.

### Acknowledgements
- Thanks to the Django community for providing extensive documentation and support.



