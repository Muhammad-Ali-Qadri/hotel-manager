# Rooms

- **ID (self generated)**
- Room Number (int)
- Type (int) (foreign key with type model)
- Occupied (bool variable)
- One night price
- Capacity (int)

# User

- **ID (self generated)**
- Name
- user type (int)
- email address
- Phone number

# Registrations

- **UserID (foreign key)**
- **RoomID (foreign key)**
- Check in time (Date)
- Check out time (Date, default = 1 day after check in)

# Room Type

- **ID (autogenrated)**
- Type id (not auto generated, other one)
- Type name
  - Executive
  - Deluxe
  - Presidential
  - Business
- Wifi (bool)
- Room service (bool)
- Breakfast (bool)
- Shuttle service (bool)
- Spa (bool)
- Mini bar (bool)
- Gym (bool)
- Pool (bool)

# images

- **Room ID**
- **Image ID** 
- URL
- Description