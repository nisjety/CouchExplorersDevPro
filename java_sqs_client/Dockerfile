# Stage 1: Build
FROM maven:3.8-openjdk-17 AS build
WORKDIR /app

# Copy only the pom.xml first to leverage Docker layer caching
COPY pom.xml .

# Resolve dependencies before copying the source code
RUN mvn dependency:go-offline -B

# Copy the source code
COPY src ./src

# Build the application
RUN mvn clean package -DskipTests

# Stage 2: Runtime
FROM openjdk:17-slim
WORKDIR /app
COPY --from=build /app/target/imagegenerator-0.0.1-SNAPSHOT.jar /app/imagegenerator.jar

# Run the application
ENTRYPOINT ["java", "-jar", "/app/imagegenerator.jar"]
