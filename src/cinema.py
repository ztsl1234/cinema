from datetime import datetime
import logging

from utils import utils
from validation_error import ValidationError

logger = logging.getLogger(__name__)

class Cinema:

    def __init__(self, movie_title:str, rows:int, seats_per_row:int):
        """
        Constructor to construct a Cinema object

        Args:
            movie_title (str): title of the moview
            rows (int): number of rows
            seats_per_row (int): number of seats in 1 row

        Raises:
            ValidationError: rows more than 26
            ValidationError: seats per row more than 50
        """

        if rows > 26:
            raise ValidationError("rows cannot be more than 26!")
        
        if seats_per_row > 50:
            raise ValidationError("seats_per_row cannot be more than 50!")

        self.movie_title=movie_title
        self.rows=rows
        self.seats_per_row=seats_per_row
        self.seating_map = [[0 for _ in range(seats_per_row)] for _ in range(rows)]   
        self.bookings = {} 

    def get_available_seats(self) -> int:
        """
        This will give the number of seats available in the cinema

        Returns:
            int: number
        """
        num_seats = 0
        for row in self.seating_map:
            for seat in row:
                if seat == 0:
                    num_seats += 1
        return num_seats
    
    def display_seating_map(self, selected_seats:list=None, booking_id_to_highlight:str=None):
        """
        Display the seating map. 
        
        If selected_seats is provided, they are shown as 'o'.
        If booking_id_to_highlight is provided, highlight those seats with 'o' and others with '#'.

        Args:
            selected_seats (list, optional): list of selected seats. Defaults to None.
            booking_id_to_highlight (str, optional): booking id to highlight on seating map Defaults to None.
        """

        print("\n          S C R E E N")
        print("--------------------------------")
        
        temp_map = [row[:] for row in self.seating_map]
        
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

    def book_tickets(self, num_tickets:int) -> tuple:
        """
        This function will book the tickets

        Args:
            num_tickets (int): number of tickets

        Raises:
            ValidationError: negative number of tickets
            ValidationError: user selected seat is not available

        Returns:
            tuple: selected seats, seating map
        """
                
        available_seats = self.get_available_seats()

        if num_tickets <= 0:
            raise ValidationError("Number of tickets cannot be negative. Please enter a positive number of tickets.")
        elif num_tickets > available_seats:
            raise ValidationError(f"Sorry, there are only {available_seats} seats available.")

        selected_seats, temp_map=self.allocate_seating(num_tickets)
            
        return selected_seats, temp_map
                                  
    def confirm_booking(self, selected_seats:list, booking_id:str, seating_map:list):
        """_summary_

        Args:
            selected_seats (list): list of selected seats
            booking_id (str): booking id
            seating_map (list): map of the seats
        """            
        self.bookings[booking_id] = selected_seats
        self.seating_map= seating_map

    def update_seat_selection(self, selected_seats:list, seat_pos:str, num_tickets:int) -> tuple:
        """
        This function will update the seat selection with the user selected seats

        Args:
            selected_seats (list): list of selected seats
            seat_pos (str): posiiton of selected seats
            num_tickets (int): number of tickets

        Raises:
            ValidationError: invalid seat selection

        Returns:
            tuple: selected seats, seating map
        """
        # Parse seat position (e.g. 'B03')
        row_letter = seat_pos[0].upper()
        col_number = int(seat_pos[1:]) - 1
        
        row_number = ord(row_letter) - ord('A')
        
        if row_number < 0 or row_number >= self.rows or col_number < 0 or col_number >= self.seats_per_row:
           raise ValidationError("Invalid seat selection. Please try again.")

        selected_seats, temp_map=self.allocate_seating(num_tickets, seat_row=row_number, seat_col=col_number)

        return selected_seats, temp_map
    
    def allocate_remaining_seats(self,remaining_tickets:int,selected_seats:list, temp_map:list ) -> tuple:
        """
        allocate remaining seats starting from row 1 col 1

        Args:
            remaining_tickets (_type_): _description_
            selected_seats (_type_): _description_
            temp_map (_type_): _description_

        Returns:
            tuple: selected seats, seating map
        """
        if remaining_tickets > 0:
            for row in range(0, self.rows):
                for col in range(0, self.seats_per_row):
                    #find empty seats
                    if temp_map[row][col] == 0:
                        selected_seats.append((row, col))
                        temp_map[row][col] = 2
                        remaining_tickets -= 1                    
                        if remaining_tickets == 0:
                            return selected_seats, temp_map
        else:
            return selected_seats,temp_map
        
    def allocate_seating(self,num_tickets:int, seat_row:int=None, seat_col:int=None) -> tuple:
        """
        This function allocates the default seating if seat_row and seat_col 
        are not passed

        Args:
            num_tickets (int): number of tickets
            seat_row (int, optional): selected seat row. Defaults to None.
            seat_col (int, optional): selected seat column. Defaults to None.

        Raises:
            ValidationError: unavailable 

        Returns:
            tuple: selected seats (list) , seating map (list)
        """
        selected_seats = []
        temp_map = [row[:] for row in self.seating_map]
        remaining_tickets=num_tickets
        middle_pos = self.seats_per_row // 2 

        # Start from furthest row from screen (first row index) if not given any row
        for row in range(0 if seat_row is None else seat_row, self.rows): 
            #selected seat given
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
                #find empty seats
                if temp_map[row][col] == 0:
                    selected_seats.append((row, col))
                    temp_map[row][col] = 2
                    remaining_tickets -= 1                    
    
                    if remaining_tickets == 0:
                        return selected_seats, temp_map
       
        #still have tickets not allocated after using default seat selection or the selected seats
        # => go through from row1 col1 again
        if remaining_tickets > 0:
            return (self.allocate_remaining_seats(remaining_tickets,selected_seats, temp_map))