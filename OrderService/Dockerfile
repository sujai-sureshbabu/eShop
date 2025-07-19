# --- Build Stage ---
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src

# Copy everything and restore dependencies
COPY . .
RUN dotnet restore

# Build and publish the app
RUN dotnet publish -c Release -o /app/publish

# --- Runtime Stage ---
FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS final
WORKDIR /app

# Copy the published app from the build stage
COPY --from=build /app/publish .

# Use default entrypoint to run your app
ENTRYPOINT ["dotnet", "OrderService.dll"]
