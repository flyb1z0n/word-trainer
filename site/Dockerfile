# Use the official Nginx image as the base image
FROM nginx:alpine

# Copy the built site files to the Nginx HTML directory
COPY dist/ /usr/share/nginx/html

# Expose port 80
EXPOSE 80