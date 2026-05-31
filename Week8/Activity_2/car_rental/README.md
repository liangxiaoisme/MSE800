# Car Rental System (Python + SQLite + Docker)

Simple CLI app to add, list, and remove cars (plate, type, year) using a SQLite database.

## Quickstart

```bash
# 1) Build the image
docker build -t car_rental .

# 2) Run the app (interactive)
docker run -it --name car_rental_app car_rental

# Optional: persist database to your host
# Linux/macOS (bash/zsh):
docker run -it --rm -v $(pwd)/cars.db:/app/cars.db car_rental
# Windows (PowerShell):
docker run -it --rm -v ${PWD}/cars.db:/app/cars.db car_rental
# Windows (cmd.exe):
docker run -it --rm -v %cd%/cars.db:/app/cars.db car_rental
```

## Menu
- Add Car
- List Cars
- Remove Car
- Exit
