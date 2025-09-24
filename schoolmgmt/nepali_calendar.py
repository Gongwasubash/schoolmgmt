from datetime import datetime, date, timedelta
import calendar

class NepaliCalendar:
    """Enhanced Nepali Calendar utility for comprehensive date conversion and formatting"""
    
    # Nepali month names
    NEPALI_MONTHS = [
        'बैशाख', 'जेठ', 'आषाढ', 'श्रावण', 'भाद्र', 'आश्विन',
        'कार्तिक', 'मंसिर', 'पौष', 'माघ', 'फाल्गुन', 'चैत्र'
    ]
    
    NEPALI_MONTHS_EN = [
        'Baisakh', 'Jestha', 'Ashadh', 'Shrawan', 'Bhadra', 'Ashwin',
        'Kartik', 'Mangsir', 'Poush', 'Magh', 'Falgun', 'Chaitra'
    ]
    
    # Nepali weekdays
    NEPALI_WEEKDAYS = [
        'आइतबार', 'सोमबार', 'मंगलबार', 'बुधबार', 'बिहिबार', 'शुक्रबार', 'शनिबार'
    ]
    
    NEPALI_WEEKDAYS_EN = [
        'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'
    ]
    
    # Comprehensive days in each Nepali month for different years
    NEPALI_DAYS = {
        2090: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        2089: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        2088: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        2087: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        2086: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        2085: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        2084: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        2083: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        2082: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        2081: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        2080: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        2079: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        2078: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        2077: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        2076: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        2075: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
    }
    
    @classmethod
    def english_to_nepali_date(cls, english_date):
        """Convert English date to approximate Nepali date"""
        if isinstance(english_date, str):
            english_date = datetime.strptime(english_date, '%Y-%m-%d').date()
        
        # Simple approximation: Add ~57 years to get Nepali year
        nepali_year = english_date.year + 57
        
        # Adjust for Nepali calendar start (mid-April)
        if english_date.month < 4 or (english_date.month == 4 and english_date.day < 14):
            nepali_year -= 1
            
        # Simple month mapping (approximate)
        month_mapping = {
            4: 1, 5: 2, 6: 3, 7: 4, 8: 5, 9: 6,
            10: 7, 11: 8, 12: 9, 1: 10, 2: 11, 3: 12
        }
        
        nepali_month = month_mapping.get(english_date.month, 1)
        nepali_day = english_date.day
        
        # Adjust day if it exceeds month limit
        max_days = cls.NEPALI_DAYS.get(nepali_year, [31]*12)[nepali_month-1]
        if nepali_day > max_days:
            nepali_day = max_days
            
        return {
            'year': nepali_year,
            'month': nepali_month,
            'day': nepali_day,
            'month_name': cls.NEPALI_MONTHS[nepali_month-1],
            'month_name_en': cls.NEPALI_MONTHS_EN[nepali_month-1]
        }
    
    @classmethod
    def format_nepali_date(cls, nepali_date_dict, format_type='full'):
        """Format Nepali date in different formats"""
        year = nepali_date_dict['year']
        month = nepali_date_dict['month']
        day = nepali_date_dict['day']
        month_name = nepali_date_dict['month_name']
        month_name_en = nepali_date_dict['month_name_en']
        
        if format_type == 'full':
            return f"{year} {month_name} {day}"
        elif format_type == 'full_en':
            return f"{day} {month_name_en}, {year}"
        elif format_type == 'short':
            return f"{year}/{month:02d}/{day:02d}"
        else:
            return f"{year}-{month:02d}-{day:02d}"
    
    @classmethod
    def get_current_nepali_date(cls):
        """Get current date in Nepali calendar"""
        today = date.today()
        return cls.english_to_nepali_date(today)
    
    @classmethod
    def get_nepali_year_range(cls, start_year=2075, end_year=2085):
        """Get list of Nepali years for dropdowns"""
        return list(range(start_year, end_year + 1))
    
    @classmethod
    def get_nepali_session_from_date(cls, english_date=None):
        """Get Nepali academic session from a given date"""
        if english_date is None:
            english_date = date.today()
        
        nepali_date_dict = cls.english_to_nepali_date(english_date)
        year = nepali_date_dict['year']
        month = nepali_date_dict['month']
        
        # Academic year starts in Baisakh (month 1)
        if month == 12:  # Chaitra - still in previous academic year
            session_start = year
            session_end = year + 1
        else:
            session_start = year
            session_end = year + 1
        
        return f"{session_start}-{str(session_end)[-2:]}"
    
    @classmethod
    def get_nepali_fiscal_year(cls, english_date=None):
        """Get Nepali fiscal year (Shrawan to Ashadh)"""
        if english_date is None:
            english_date = date.today()
        
        nepali_date_dict = cls.english_to_nepali_date(english_date)
        year = nepali_date_dict['year']
        month = nepali_date_dict['month']
        
        # Fiscal year starts in Shrawan (month 4) and ends in Ashadh (month 3)
        if month >= 4:  # Shrawan onwards
            fiscal_start = year
            fiscal_end = year + 1
        else:  # Baisakh to Ashadh
            fiscal_start = year - 1
            fiscal_end = year
        
        return f"{fiscal_start}/{str(fiscal_end)[-2:]}"
    
    @classmethod
    def get_nepali_weekday(cls, english_date):
        """Get Nepali weekday from English date"""
        if isinstance(english_date, str):
            english_date = datetime.strptime(english_date, '%Y-%m-%d').date()
        
        weekday_index = english_date.weekday()
        # Convert Monday=0 to Sunday=0 format
        nepali_weekday_index = (weekday_index + 1) % 7
        
        return {
            'index': nepali_weekday_index,
            'name_nepali': cls.NEPALI_WEEKDAYS[nepali_weekday_index],
            'name_english': cls.NEPALI_WEEKDAYS_EN[nepali_weekday_index]
        }
    
    @classmethod
    def get_nepali_today_info(cls):
        """Get comprehensive today's Nepali date information"""
        today = date.today()
        nepali_date = cls.english_to_nepali_date(today)
        weekday = cls.get_nepali_weekday(today)
        session = cls.get_nepali_session_from_date(today)
        fiscal_year = cls.get_nepali_fiscal_year(today)
        
        return {
            'english_date': today,
            'nepali_date': nepali_date,
            'weekday': weekday,
            'session': session,
            'fiscal_year': fiscal_year,
            'formatted_full': cls.format_nepali_date(nepali_date, 'full_en'),
            'formatted_short': cls.format_nepali_date(nepali_date, 'short'),
            'is_weekend': weekday['index'] == 6  # Saturday is weekend in Nepal
        }
    
    @classmethod
    def nepali_date_to_english_approximate(cls, nepali_year, nepali_month, nepali_day):
        """Convert Nepali date to approximate English date"""
        # Simple approximation: subtract ~57 years
        english_year = nepali_year - 57
        
        # Reverse month mapping
        month_mapping = {
            1: 4, 2: 5, 3: 6, 4: 7, 5: 8, 6: 9,
            7: 10, 8: 11, 9: 12, 10: 1, 11: 2, 12: 3
        }
        
        english_month = month_mapping.get(nepali_month, 1)
        
        # Adjust year for months 10, 11, 12 (Jan, Feb, Mar)
        if nepali_month >= 10:
            english_year += 1
        
        # Ensure valid day
        try:
            max_days = calendar.monthrange(english_year, english_month)[1]
            english_day = min(nepali_day, max_days)
            return date(english_year, english_month, english_day)
        except:
            return date(english_year, english_month, 1)
    
    @classmethod
    def get_nepali_year_sessions(cls, start_year=2082, end_year=2100):
        """Get list of Nepali academic sessions"""
        sessions = []
        for year in range(start_year, end_year + 1):
            sessions.append({
                'value': f"{year}-{str(year+1)[-2:]}",
                'label': f"{year}-{str(year+1)[-2:]} BS",
                'start_year': year,
                'end_year': year + 1
            })
        return sessions
    
    @classmethod
    def get_nepali_calendar_month(cls, year, month):
        """Get full calendar for a Nepali month"""
        if year not in cls.NEPALI_DAYS:
            return None
        
        days_in_month = cls.NEPALI_DAYS[year][month-1]
        
        # Get first day of month in English to determine starting weekday
        first_day_english = cls.nepali_date_to_english_approximate(year, month, 1)
        first_weekday = cls.get_nepali_weekday(first_day_english)['index']
        
        calendar_data = {
            'year': year,
            'month': month,
            'month_name': cls.NEPALI_MONTHS[month-1],
            'month_name_en': cls.NEPALI_MONTHS_EN[month-1],
            'days_in_month': days_in_month,
            'first_weekday': first_weekday,
            'weeks': []
        }
        
        # Generate calendar weeks
        week = [None] * first_weekday  # Empty cells before first day
        
        for day in range(1, days_in_month + 1):
            week.append(day)
            if len(week) == 7:
                calendar_data['weeks'].append(week)
                week = []
        
        # Fill remaining cells in last week
        if week:
            while len(week) < 7:
                week.append(None)
            calendar_data['weeks'].append(week)
        
        return calendar_data
    
    @classmethod
    def is_valid_nepali_date(cls, year, month, day):
        """Validate Nepali date"""
        if year not in cls.NEPALI_DAYS:
            return False
        if month < 1 or month > 12:
            return False
        if day < 1 or day > cls.NEPALI_DAYS[year][month-1]:
            return False
        return True
    
    @classmethod
    def format_nepali_datetime(cls, english_datetime, format_type='full'):
        """Format datetime with Nepali date and time"""
        if isinstance(english_datetime, str):
            english_datetime = datetime.strptime(english_datetime, '%Y-%m-%d %H:%M:%S')
        
        nepali_date = cls.english_to_nepali_date(english_datetime.date())
        time_str = english_datetime.strftime('%H:%M:%S')
        
        if format_type == 'full':
            return f"{cls.format_nepali_date(nepali_date, 'full_en')} {time_str}"
        elif format_type == 'short':
            return f"{cls.format_nepali_date(nepali_date, 'short')} {time_str}"
        else:
            return f"{cls.format_nepali_date(nepali_date, format_type)} {time_str}"
    
    @classmethod
    def get_nepali_events_calendar(cls, year, month):
        """Get events calendar for a Nepali month (can be extended for festivals)"""
        calendar_data = cls.get_nepali_calendar_month(year, month)
        if not calendar_data:
            return None
        
        # Add common Nepali festivals (basic implementation)
        festivals = {
            1: {1: 'New Year', 15: 'Buddha Jayanti'},  # Baisakh
            7: {15: 'Dashain'},  # Ashwin
            8: {15: 'Tihar'},    # Kartik
        }
        
        calendar_data['events'] = festivals.get(month, {})
        return calendar_data
    
    @classmethod
    def add_nepali_days(cls, nepali_date_dict, days):
        """Add days to a Nepali date"""
        year = nepali_date_dict['year']
        month = nepali_date_dict['month']
        day = nepali_date_dict['day'] + days
        
        # Handle month overflow
        while day > cls.NEPALI_DAYS.get(year, [31]*12)[month-1]:
            day -= cls.NEPALI_DAYS.get(year, [31]*12)[month-1]
            month += 1
            if month > 12:
                month = 1
                year += 1
        
        # Handle negative days
        while day <= 0:
            month -= 1
            if month <= 0:
                month = 12
                year -= 1
            day += cls.NEPALI_DAYS.get(year, [31]*12)[month-1]
        
        return {
            'year': year,
            'month': month,
            'day': day,
            'month_name': cls.NEPALI_MONTHS[month-1],
            'month_name_en': cls.NEPALI_MONTHS_EN[month-1]
        }
    
    @classmethod
    def get_nepali_date_range(cls, start_date, end_date):
        """Get list of Nepali dates between two English dates"""
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        dates = []
        current_date = start_date
        
        while current_date <= end_date:
            nepali_date = cls.english_to_nepali_date(current_date)
            dates.append({
                'english_date': current_date,
                'nepali_date': nepali_date,
                'formatted': cls.format_nepali_date(nepali_date, 'full_en')
            })
            current_date += timedelta(days=1)
        
        return dates