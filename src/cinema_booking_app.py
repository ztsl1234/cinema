import logging
from datetime import datetime, timedelta

from utils import utils
from cinema import Cinema
from validation_error import ValidationError

logger = logging.getLogger(__name__)

"""
# GIC Cinemas Booking System

## Ticket Booking

When user selects [1], the booking "workflow" should start. User needs to input the desired number of tickets they want to book. If there are not enough seats available, user should be allowed to try again.

After seats are allocated, a booking id should be generated and displayed along with the number of tickets booked and the seating map showing default selected seats. The seats reserved for the current booking should be marked differently than seats taken by existing bookings.

Use the following rules for default seat choice:

- Start from furthest row from the screen.
- Start from the middle-most possible col.
- When a row is not enough to accomodate the number of tickets, it should overflow to the next row closer to the screen.

User can choose another seating position by specifying the starting position of the seats. Seating assignment should follow this rule:

- Starting from the specified position, fill up all empty seats in the same row all the way to the right of the cinema hall.
- When there is not enough seats available, it should overflow to the next row closer to the screen.
- Seat allocation for overflow follows the rules for default seat choice.

"""
class CinemaBookingApp:
    def __init__(self):
        self.next_booking_id = 1

    def run(self):

        #Setup cinema
        print("Please define movie title and seating map in [Title] [Row] [SeatsPerRow] format:")

        loop_flag=True
        while loop_flag:
            try:
                cinema_inputs = input("> ")
                input_parts = cinema_inputs.split(maxsplit=2)
                title = input_parts[0]
                rows = int(input_parts[1])
                seats_per_row = int(input_parts[2])

                cinema=Cinema(title, rows, seats_per_row)
                self.cinema=cinema
                loop_flag=False   
            except ValueError as e:
                print(f"Invalid input format - {str(e)}. Please use [Title] [Row] [SeatsPerRow] format.")
        
        # Main application loop
        loop_flag = True
        while loop_flag:
            available_seats = cinema.get_available_seats()
            print(f"\nWelcome to GIC Cinemas")
            print(f"[1] Book tickets for {cinema.movie_title} ({available_seats} seats available)")
            print("[2] Check bookings")
            print("[3] Exit")
            print("Please enter your choice:")
            
            choice = input("> ")
            
            if choice == "1":
                # Book tickets
                self.booking_tickets()
            
            elif choice == "2":
                # Check bookings
                self.check_bookings()
            
            elif choice == "3":
                # Exit
                print("\nThank you for using GIC Cinemas system. Bye!")
                loop_flag = False
            
            else:
                print("Invalid choice. Please try again.")

    def booking_tickets(self):
        """
        This function will handle the booking of tickets in the cinema
        """
        
        loop_flag=True
        while loop_flag:
            print("\nEnter number of tickets to book, or enter blank to go back to main menu:")
            num_tickets_input = input("> ")
            
            if not num_tickets_input:
                loop_flag=False
            else:            
                try:                    
                    num_tickets = int(num_tickets_input)
                    
                    selected_seats, temp_map = self.cinema.book_tickets(num_tickets)
 
                    booking_id = self.generate_booking_id()
                        
                    print(f"\nSuccessfully reserved {num_tickets} {self.cinema.movie_title} tickets.")
                    print(f"Booking id: {booking_id}")
                    print("Selected seats:")                    
                    self.cinema.display_seating_map(selected_seats)
                    
                    selected_seats,temp_map=self.change_seats(selected_seats,num_tickets, booking_id,temp_map )

                    # Confirm booking
                    self.cinema.confirm_booking(selected_seats, booking_id, seating_map=temp_map)
                    print(f"\nBooking id: {booking_id} confirmed.")
                    loop_flag=False

                except (ValueError) as e:
                    print("Invalid input. Please enter a number.")
                except (ValidationError) as e:
                    print(f"{str(e)}")                    

    def change_seats(self, selected_seats:list, num_tickets:int, booking_id:str, seating_map:list) -> tuple:
        """
        This function allow user to change the seat selection

        Args:
            selected_seats (list): list of coordinates of the seats selected
            num_tickets (int): number of tickets
            booking_id (str): booking id
            seating_map (list): list of seats in cinema

        Returns:
            tuple: selected seats (list), map containing the selected seats
        """

        loop_flag=True
        while loop_flag:
            print("Enter blank to accept seat selection, or enter new seating position:")
            new_pos = input("> ")
            
            if not new_pos:
                return (selected_seats,seating_map)
            else:
                try:
                    new_selected_seats, new_temp_map = self.cinema.update_seat_selection(selected_seats, new_pos, num_tickets)
                
                    if new_selected_seats:
                        selected_seats = new_selected_seats
                        seating_map = new_temp_map
                        
                        print("change")
                        print(f"Booking id: {booking_id}")
                        print("Selected seats:")                    
                        self.cinema.display_seating_map(selected_seats)
                
                except (ValidationError) as e:
                    print(f"{str(e)}\n")                      

    def check_bookings(self):
        """
        This function allows user to check on the bookings that they had made.
        """
        
        loop_flag=True
        while loop_flag:
            print("\nEnter booking id, or enter blank to go back to main menu:")
            booking_id = input("> ")
            
            if not booking_id:
                loop_flag=False
            elif booking_id in self.cinema.bookings:
                print(f"\nBooking id: {booking_id}")
                print("Selected seats:")
                self.cinema.display_seating_map(booking_id_to_highlight=booking_id)
            else:
                print("Booking not found.")        

    def generate_booking_id(self):
        """
        This function retrieve a new booking id and include the booking counter by 1

        Returns:
            _type_: _description_
        """
        booking_id = f"GIC{self.next_booking_id:04d}"
        self.next_booking_id += 1
        return booking_id