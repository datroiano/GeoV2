from datetime import date, datetime, timedelta


class GetDate:

    @staticmethod
    def get_date_next_friday(input_date=None):
        if input_date is None:
            today = date.today()
        else:
            today = datetime.strptime(input_date, '%Y-%m-%d').date()

        days_until_friday = (4 - today.weekday()) % 7  # Calculate days until next Friday (0=Monday, 1=Tuesday)
        if days_until_friday == 0:
            days_until_friday = 7  # If today is Friday, move to next Friday
        next_friday_date = today + timedelta(days=days_until_friday)
        formatted_date = next_friday_date.strftime('%Y-%m-%d')

        return formatted_date

    @staticmethod
    def get_date_next_third_friday(input_date):
        date_obj = datetime.strptime(input_date, '%Y-%m-%d')
        day_of_week = date_obj.weekday()
        days_until_friday = (4 - day_of_week) % 7
        first_friday = date_obj + timedelta(days=days_until_friday)
        third_friday = first_friday + timedelta(weeks=2)

        if third_friday.month != date_obj.month:
            next_month = date_obj.replace(day=1) + timedelta(days=32)
            third_friday = next_month.replace(day=1)

            while third_friday.weekday() != 4:
                third_friday += timedelta(days=1)

            third_friday += timedelta(weeks=2)

        return third_friday.strftime('%Y-%m-%d')

    @staticmethod
    def get_date_day_before(date_string):  # With logic to deal with Mondays (reverts to previous Friday)
        input_date = datetime.strptime(date_string, '%Y-%m-%d')

        if input_date.weekday() == 0:
            previous_day = input_date - timedelta(days=3)
        else:
            previous_day = input_date - timedelta(days=1)

        return previous_day.strftime('%Y-%m-%d')

    @staticmethod
    def get_date_31_days_ago():
        current_date = datetime.now().date()
        date_31_days_ago = current_date - timedelta(days=31)
        formatted_date = date_31_days_ago.strftime('%Y-%m-%d')

        return formatted_date

    @staticmethod
    def get_today_date():
        return datetime.now().date().strftime('%Y-%m-%d')

