from datetime import datetime
import logging

from utils import utils
from validation_error import ValidationError

logger = logging.getLogger(__name__)

class Cinema:

    def __init__(self, movie_title:str, rows:int, seats_per_row:int):

        if rows > 26:
            raise ValidationError("rows cannot be more than 26!")
        
        if seats_per_row > 50:
            raise ValidationError("seats_per_row cannot be more than 50!")

        self.movie_title=movie_title
        self.rows=rows
        self.seats_per_row=seats_per_row
        self.seating_map = [[0 for _ in range(seats_per_row)] for _ in range(rows)]   
        self.bookings = {} 

    def get_available_seats(self) -> dict:
        num_seats = 0
        for row in self.seating_map:
            for seat in row:
                if seat == 0:
                    num_seats += 1
        return num_seats
    
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

    def book_tickets(self, num_tickets):
                
        available_seats = self.get_available_seats()

        if num_tickets <= 0:
            raise ValidationError("Number of tickets cannot be negative. Please enter a positive number of tickets.")
        elif num_tickets > available_seats:
            raise ValidationError(f"Sorry, there are only {available_seats} seats available.")

        # Generate default seat selection
        selected_seats = []
        temp_map = [row[:] for row in self.seating_map]
        
        # Start from furthest row from screen (first row index)
        for row in range(0, self.rows - 1, 1):
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
    
    def confirm_booking(self, selected_seats, booking_id, seating_map):
            print("seating_map")
            print(seating_map)
            self.bookings[booking_id] = selected_seats
            self.seating_map= seating_map

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
    