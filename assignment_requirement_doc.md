Implementation Question

URL Shortener
Build an application that allows generating short URLs for any given URL for a logged-in user.
The application should:

1. Allow the user to create short URLs 
2. Generate short URL code for each request without using any library (implement a custom algorithm for short
   URL generation),
3. Log IP address, user agent and time of access each time the short URL is used,
4. All expired or invalid short URLs should return 404,
5. Display all the short URLs created by the user and their usage, if any, to the creator of the short URLs.

Each short URL creation request should mandatory specify:

1. The URL to be shortened,
2. An expiry from 1 hour to 1 year,
    1. The expiry can be defined in terms of duration (days, hours, mins and seconds) OR an absolute time,
    2. The application should verify that the computed or absolute expiry time lies within the limits.
3. Whether the short URL can be used only once (it is unavailable after the first use)
    1. If the short URL is for one-time use, the application must restrict parallel requests and only serve the
       first one.
    2. One-time use can be extended to a usage for a specific number of times as well.

The application with all of its dependencies should be built into Docker images with a Docker compose file, for
easy deployment.

Advanced test:
As the application would be deployed through Docker images, the application should have self-redeployment
capabilities, so that each time the Docker image is updated, an API call to the application at a specific
endpoint, with specific credentials would trigger a redeployment of the Docker images.