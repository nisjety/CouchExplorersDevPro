# Stage 1: Build
FROM maven:3.8-openjdk-17 AS build
WORKDIR /app

# Copy the pom.xml and src directory directly from the current directory
COPY pom.xml .
COPY src ./src

# Download dependencies
RUN mvn dependency:go-offline -B

# Build the application
RUN mvn clean package -DskipTests

# Stage 2: Runtime
FROM openjdk:17-slim
WORKDIR /app
COPY --from=build /app/target/imagegenerator-0.0.1-SNAPSHOT.jar /app/imagegenerator.jar

# Run the application
ENTRYPOINT ["java", "-jar", "/app/imagegenerator.jar"]
