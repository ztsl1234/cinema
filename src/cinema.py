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

        print(temp_map)
        
        if selected_seats:
            for row, col in selected_seats:
                temp_map[row][col] = 9
        
        highlight_seats = None
        if booking_id_to_highlight and booking_id_to_highlight in self.bookings:
            highlight_seats = self.bookings[booking_id_to_highlight]

        # Mark selected seats for this booking
        if highlight_seats:
            for row, col in highlight_seats:
                temp_map[row][col] = 9

        # Display the map
        for i in range(self.rows - 1, -1, -1):
            row_letter = chr(ord('A') + i)
            print(f"{row_letter}", end=" ")
            
            for j in range(self.seats_per_row):
                if temp_map[i][j]==0:
                    print(". ", end=" ")
                elif temp_map[i][j]==2:
                    print("# ", end=" ")
                else:
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

        selected_seats, temp_map=self.allocate_seating(num_tickets)
        
        remaining_tickets = num_tickets - len(selected_seats)
        print(remaining_tickets)

        # # Generate default seat selection
        # selected_seats = []
        # temp_map = [row[:] for row in self.seating_map]
        # remaining_tickets=num_tickets
        
        # consecutive_seats = 0
        # # Start from furthest row from screen (first row index)
        # #for row in range(0, self.rows - 1, 1): #???
        # for row in range(0, self.rows): #???
        #     print(f"row={row}")
        #     print(f"temp_map={temp_map}")
        #     # Calculate middle position to start
        #     middle = self.seats_per_row // 2 - (remaining_tickets // 2)
        #     #middle = self.seats_per_row // 2 
        #     print(f"middle={middle}")

        #     #if start from middle not enough to accomodate all the tickets => start from col 1
        #     if (remaining_tickets >= self.seats_per_row) :
        #     # if (remaining_tickets >= self.seats_per_row) or (remaining_tickets > middle):
        #     # if middle < 0: 
        #         middle = 0
            
        #     for col in range(middle, self.seats_per_row):
        #         print(f"col={col}")
        #         print(f"temp_map={temp_map}")
        #         #find empty seats
        #         if temp_map[row][col] == 0:
        #             selected_seats.append((row, col))
        #             temp_map[row][col] = 2
        #             remaining_tickets -= 1                    
        #             consecutive_seats += 1
        #             print(f"consecutive_seats={consecutive_seats}")
        #             print(f"remaining_tickets={remaining_tickets}")        
        #             if remaining_tickets == 0:
        #                 return selected_seats, temp_map

        print("out of all loops!")          
        #still have tickets not allocated after using default seat selection
        # => go through from row1 again and fill from col1
        if remaining_tickets > 0:
            selected_seats, temp_map =self.allocate_remaining_seats(remaining_tickets,selected_seats, temp_map)
        
        return selected_seats, temp_map
                          
        #still have tickets not allocated => go through from row1 again and fill from col1
        # if remaining_tickets > 0:
        #     for row in range(0, self.rows):
        #         print(f"row={row}")
        #         print(f"temp_map={temp_map}")
        #         for col in range(0, self.seats_per_row):
        #             print(f"col={col}")
        #             print(f"temp_map={temp_map}")
        #             #find empty seats
        #             if temp_map[row][col] == 0:
        #                 selected_seats.append((row, col))
        #                 temp_map[row][col] = 2
        #                 remaining_tickets -= 1                    
        #                 print(f"remaining_tickets={remaining_tickets}")        
        #                 if remaining_tickets == 0:
        #                     return selected_seats, temp_map
        
    def confirm_booking(self, selected_seats, booking_id, seating_map):
            self.bookings[booking_id] = selected_seats
            self.seating_map= seating_map

    def update_seat_selection(self, selected_seats, seat_pos, num_tickets):
        # Parse seat position (e.g. 'B03')
        row_letter = seat_pos[0].upper()
        col_number = int(seat_pos[1:]) - 1
        
        row_number = ord(row_letter) - ord('A')
        
        if row_number < 0 or row_number >= self.rows or col_number < 0 or col_number >= self.seats_per_row:
           raise ValidationError("Invalid seat selection. Please try again.")

        selected_seats, temp_map=self.allocate_seating(num_tickets, seat_row=row_number, seat_col=col_number)

        return selected_seats, temp_map

        # temp_map = [row[:] for row in self.seating_map]
        # new_selected_seats = []
        # remaining_tickets = num_tickets

        # #check if selected seat is available
        # if temp_map[row_number][col_number] > 0:
        #     raise ValidationError("The seat is unavailable. Please re-select.")

        # # Try to allocate seats starting from the specified position
        # for r in range(row_number, self.rows):
        #     for c in range(col_number if r == row_number else 0, self.seats_per_row):
        #         if temp_map[r][c] == 0:
        #             new_selected_seats.append((r, c))
        #             temp_map[r][c] = 2
        #             remaining_tickets -= 1
        #             if remaining_tickets == 0:
        #                 return new_selected_seats, temp_map
        
        
        # #still have tickets not allocated after using default seat selection
        # # => go through from row1 again and fill from col1
        # if remaining_tickets > 0:
        #     return (self.allocate_remaining_seats(remaining_tickets,selected_seats, temp_map))
    
    def allocate_remaining_seats(self,remaining_tickets,selected_seats, temp_map ):
        """
        allocate remaining seats starting from row 1 col 1

        Args:
            remaining_tickets (_type_): _description_
            selected_seats (_type_): _description_
            temp_map (_type_): _description_

        Returns:
            _type_: _description_
        """
    
        if remaining_tickets > 0:
            for row in range(0, self.rows):
                print(f"row={row}")
                print(f"temp_map={temp_map}")
                for col in range(0, self.seats_per_row):
                    print(f"col={col}")
                    print(f"temp_map={temp_map}")
                    #find empty seats
                    if temp_map[row][col] == 0:
                        selected_seats.append((row, col))
                        temp_map[row][col] = 2
                        remaining_tickets -= 1                    
                        print(f"remaining_tickets={remaining_tickets}")        
                        if remaining_tickets == 0:
                            return selected_seats, temp_map
        else:
            return selected_seats,temp_map
        
    def xxxallocate_default_seating(self,num_tickets):
        """
        

        Args:
            num_tickets (_type_): _description_

        Returns:
            _type_: _description_
        """
        # Generate default seat selection
        selected_seats = []
        temp_map = [row[:] for row in self.seating_map]
        remaining_tickets=num_tickets
        middle_pos = self.seats_per_row // 2 
        print(f"middle_pos={middle_pos}")        
        
        consecutive_seats = 0
        # Start from furthest row from screen (first row index)
        #for row in range(0, self.rows - 1, 1): #???
        for row in range(0, self.rows): #???
            print(f"row={row}")
            print(f"temp_map={temp_map}")

            #if required seats more than 1 row => start from col 1
            if (remaining_tickets >= self.seats_per_row) :
                start_col = 0

            # Calculate middle position to start
            # middle = self.seats_per_row // 2 - (remaining_tickets // 2)

            #if middle seat is taken => start from the available seats to the rt of middle seat
            # so that group will not be separated
            if temp_map[row][middle_pos] > 0:
                start_col= middle_pos+1
            else:
                start_col= middle_pos - (remaining_tickets // 2) #select middle seats for the group
            
            for col in range(start_col, self.seats_per_row):
                print(f"col={col}")
                print(f"temp_map={temp_map}")
                #find empty seats
                if temp_map[row][col] == 0:
                    selected_seats.append((row, col))
                    temp_map[row][col] = 2
                    remaining_tickets -= 1                    
                    consecutive_seats += 1
                    print(f"consecutive_seats={consecutive_seats}")
                    print(f"remaining_tickets={remaining_tickets}")        
                    if remaining_tickets == 0:
                        return selected_seats, temp_map

        print("out of all loops!")          
        #still have tickets not allocated after using default seat selection
        # => go through from row1 again and fill from col1
        if remaining_tickets > 0:
            return (self.allocate_remaining_seats(remaining_tickets,selected_seats, temp_map))
        

    def allocate_seating(self,num_tickets, seat_row=None, seat_col=None):
        """
        

        Args:
            num_tickets (_type_): _description_

        Returns:
            _type_: _description_
        """
        # Generate default seat selection
        selected_seats = []
        temp_map = [row[:] for row in self.seating_map]
        remaining_tickets=num_tickets
        middle_pos = self.seats_per_row // 2 
        print(f"middle_pos={middle_pos}")        
        

        consecutive_seats = 0
        # Start from furthest row from screen (first row index) if not given any row
        #for row in range(0, lf.rows - 1, 1): #???
        for row in range(0 if seat_row is None else seat_row, self.rows): #???
            print(f"row={row}")
            print(f"temp_map={temp_map}")

            #selected seat
            if seat_col is not None and row==seat_row and seat_col is not None:
                #check if selected seat is available
                if temp_map[seat_row][seat_col] > 0:
                    raise ValidationError("The seat is unavailable. Please re-select.")                
                start_col=seat_col
            #no selected seat
            else:
                #if middle seat is taken => start from the available seats to the rt of middle seat
                # so that group will not be separated
                if temp_map[row][middle_pos] > 0:
                    start_col= middle_pos+1
                else:
                    #if required seats more than 1 row => start from col 1
                    if (remaining_tickets >= self.seats_per_row) :
                        start_col = 0
                    else:
                        #select middle seats for the group
                        start_col= middle_pos - (remaining_tickets // 2) 
 
            for col in range(start_col, self.seats_per_row):
                print(f"col={col}")
                print(f"temp_map={temp_map}")
                #find empty seats
                if temp_map[row][col] == 0:
                    selected_seats.append((row, col))
                    temp_map[row][col] = 2
                    remaining_tickets -= 1                    
                    consecutive_seats += 1
                    print(f"consecutive_seats={consecutive_seats}")
                    print(f"remaining_tickets={remaining_tickets}")        
                    if remaining_tickets == 0:
                        return selected_seats, temp_map

        print("out of all loops!")          
        #still have tickets not allocated after using default seat selection
        # => go through from row1 again and fill from col1
        if remaining_tickets > 0:
            return (self.allocate_remaining_seats(remaining_tickets,selected_seats, temp_map))
        