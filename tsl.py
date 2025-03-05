class CinemaBookingSystem:
    def __init__(self):
        self.movie_title = ""
        self.rows = 0
        self.seats_per_row = 0
        self.bookings = {}
        self.next_booking_id = 1
        self.seating_map = []
        
    def initialize_cinema(self, title, rows, seats_per_row):
        if rows > 26 or seats_per_row > 50:
            return False
        
        self.movie_title = title
        self.rows = rows
        self.seats_per_row = seats_per_row
        self.seating_map = [[0 for _ in range(seats_per_row)] for _ in range(rows)]
        return True
    
    def get_available_seats(self):
        count = 0
        for row in self.seating_map:
            for seat in row:
                if seat == 0:
                    count += 1
        return count
    
    def generate_booking_id(self):
        booking_id = f"GIC{self.next_booking_id:04d}"
        self.next_booking_id += 1
        return booking_id
    
    def book_tickets(self, num_tickets):
        available_seats = self.get_available_seats()
        if num_tickets > available_seats:
            return None, None
        
        # Generate default seat selection
        selected_seats = []
        temp_map = [row[:] for row in self.seating_map]
        
        # Start from furthest row (highest row index)
        for row in range(self.rows - 1, -1, -1):
            # Calculate middle position to start
            middle = self.seats_per_row // 2 - (num_tickets // 2)
            if middle < 0:
                middle = 0
            
            consecutive_seats = 0
            for col in range(middle, self.seats_per_row):
                if temp_map[row][col] == 0:
                    consecutive_seats += 1
                    if consecutive_seats == num_tickets:
                        # Found enough consecutive seats in this row
                        for i in range(num_tickets):
                            selected_seats.append((row, col - num_tickets + 1 + i))
                            temp_map[row][col - num_tickets + 1 + i] = 2  # Mark as selected for current booking
                        return selected_seats, temp_map
                else:
                    consecutive_seats = 0
            
            # If not enough consecutive seats in this row, try next row
            remaining_tickets = num_tickets
            col = middle
            while remaining_tickets > 0 and col < self.seats_per_row:
                if temp_map[row][col] == 0:
                    selected_seats.append((row, col))
                    temp_map[row][col] = 2
                    remaining_tickets -= 1
                col += 1
            
            # If we've used all seats in this row but still need more, continue to next row
            if remaining_tickets == 0:
                return selected_seats, temp_map
            
            # If we couldn't fit all seats in this row, reset and try the next row
            if remaining_tickets < num_tickets:
                # Undo the partial allocation
                for seat in selected_seats:
                    temp_map[seat[0]][seat[1]] = 0
                selected_seats = []
    
    def update_seat_selection(self, selected_seats, seat_pos, num_tickets):
        # Parse seat position (e.g. 'B03')
        row_letter = seat_pos[0].upper()
        col_number = int(seat_pos[1:]) - 1
        
        row_idx = ord(row_letter) - ord('A')
        
        if row_idx < 0 or row_idx >= self.rows or col_number < 0 or col_number >= self.seats_per_row:
            return None, None
        
        temp_map = [row[:] for row in self.seating_map]
        new_selected_seats = []
        remaining_tickets = num_tickets
        
        # Try to allocate seats starting from the specified position
        for r in range(row_idx, self.rows):
            for c in range(col_number if r == row_idx else 0, self.seats_per_row):
                if temp_map[r][c] == 0:
                    new_selected_seats.append((r, c))
                    temp_map[r][c] = 2
                    remaining_tickets -= 1
                    if remaining_tickets == 0:
                        return new_selected_seats, temp_map
        
        # If we couldn't allocate all tickets, reset
        if remaining_tickets > 0:
            return selected_seats, None
        
        return new_selected_seats, temp_map
    
    def confirm_booking(self, selected_seats, booking_id):
        self.bookings[booking_id] = selected_seats
        
        # Update the seating map with confirmed booking
        for row, col in selected_seats:
            self.seating_map[row][col] = 1
    
    def get_booking(self, booking_id):
        return self.bookings.get(booking_id, None)
    
    def display_seating_map(self, selected_seats=None, booking_id_to_highlight=None):
        """
        Display the seating map. If selected_seats is provided, they are shown as 'o'.
        If booking_id_to_highlight is provided, highlight those seats with 'o' and others with '#'.
        """
        print("\n          S C R E E N")
        print("--------------------------------")
        
        temp_map = [row[:] for row in self.seating_map]
        
        # Mark selected seats for this booking
        if selected_seats:
            for row, col in selected_seats:
                temp_map[row][col] = 2  # 2 for currently selected seats
        
        highlight_seats = None
        if booking_id_to_highlight and booking_id_to_highlight in self.bookings:
            highlight_seats = self.bookings[booking_id_to_highlight]
        
        # Display the map
        for i in range(self.rows - 1, -1, -1):
            row_letter = chr(ord('A') + i)
            print(f"{row_letter}", end=" ")
            
            for j in range(self.seats_per_row):
                if highlight_seats:
                    if (i, j) in highlight_seats:
                        print("o ", end=" ")
                    elif temp_map[i][j] != 0:
                        print("# ", end=" ")
                    else:
                        print(". ", end=" ")
                else:
                    if temp_map[i][j] == 0:
                        print(". ", end=" ")
                    elif temp_map[i][j] == 1:
                        print("# ", end=" ")
                    elif temp_map[i][j] == 2:
                        print("o ", end=" ")
            print()
        
        print("  ", end="")
        for j in range(1, self.seats_per_row + 1):
            print(f"{j:<3}", end="")
        print("\n")


def main():
    cinema = CinemaBookingSystem()
    
    # Application start
    print("Please define movie title and seating map in [Title] [Row] [SeatsPerRow] format:")
    while True:
        try:
            init_input = input("> ")
            parts = init_input.split(maxsplit=2)
            title = parts[0]
            rows = int(parts[1])
            seats_per_row = int(parts[2])
            
            if cinema.initialize_cinema(title, rows, seats_per_row):
                break
            else:
                print("Invalid input. Maximum number of rows is 26, and maximum number of seats per row is 50.")
        except (ValueError, IndexError):
            print("Invalid input format. Please use [Title] [Row] [SeatsPerRow] format.")
    
    # Main application loop
    running = True
    while running:
        available_seats = cinema.get_available_seats()
        print(f"\nWelcome to GIC Cinemas")
        print(f"[1] Book tickets for {cinema.movie_title} ({available_seats} seats available)")
        print("[2] Check bookings")
        print("[3] Exit")
        print("Please enter your selection:")
        
        selection = input("> ")
        
        if selection == "1":
            # Book tickets
            while True:
                print("\nEnter number of tickets to book, or enter blank to go back to main menu:")
                ticket_input = input("> ")
                
                if not ticket_input:
                    break
                
                try:
                    num_tickets = int(ticket_input)
                    available_seats = cinema.get_available_seats()
                    
                    if num_tickets <= 0:
                        print("Please enter a positive number of tickets.")
                    elif num_tickets > available_seats:
                        print(f"Sorry, there are only {available_seats} seats available.")
                    else:
                        selected_seats, temp_map = cinema.book_tickets(num_tickets)
                        booking_id = cinema.generate_booking_id()
                        
                        print(f"\nSuccessfully reserved {num_tickets} {cinema.movie_title} tickets.")
                        print(f"Booking id: {booking_id}")
                        print("Selected seats:")
                        
                        cinema.display_seating_map(selected_seats)
                        
                        # Allow user to change seat selection
                        while True:
                            print("Enter blank to accept seat selection, or enter new seating position:")
                            new_pos = input("> ")
                            
                            if not new_pos:
                                break
                            
                            new_selected_seats, new_temp_map = cinema.update_seat_selection(selected_seats, new_pos, num_tickets)
                            
                            if new_selected_seats:
                                selected_seats = new_selected_seats
                                temp_map = new_temp_map
                                
                                print(f"\nBooking id: {booking_id}")
                                print("Selected seats:")
                                cinema.display_seating_map(selected_seats)
                            else:
                                print("Invalid seat selection. Please try again.")
                        
                        # Confirm booking
                        cinema.confirm_booking(selected_seats, booking_id)
                        print(f"\nBooking id: {booking_id} confirmed.")
                        break
                        
                except ValueError:
                    print("Invalid input. Please enter a number.")
        
        elif selection == "2":
            # Check bookings
            while True:
                print("\nEnter booking id, or enter blank to go back to main menu:")
                booking_id = input("> ")
                
                if not booking_id:
                    break
                
                if booking_id in cinema.bookings:
                    print(f"\nBooking id: {booking_id}")
                    print("Selected seats:")
                    cinema.display_seating_map(booking_id_to_highlight=booking_id)
                else:
                    print("Booking not found.")
        
        elif selection == "3":
            # Exit
            print("\nThank you for using GIC Cinemas system. Bye!")
            running = False
        
        else:
            print("Invalid selection. Please try again.")


if __name__ == "__main__":
    main()