import logging
from datetime import datetime

from cinema_booking_app import CinemaBookingApp

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    app = CinemaBookingApp()
    app.run()