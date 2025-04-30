import React, { Component } from 'react';
import "../css/calender.css";

class Calendar extends Component {
  constructor(props) {
    super(props);
    const today = new Date();
    this.state = {
      currentMonth: today.getMonth(),
      currentYear: today.getFullYear(),
      todayDate: today.getDate(),
      todayMonth: today.getMonth(),
      todayYear: today.getFullYear(),
    };
  }

  // Function to get the number of days in the current month
  getDaysInMonth(month, year) {
    return new Date(year, month + 1, 0).getDate();
  }

  // Function to handle next month
  nextMonth = () => {
    this.setState((prevState) => ({
      currentMonth: (prevState.currentMonth + 1) % 12,
      currentYear: prevState.currentMonth === 11 ? prevState.currentYear + 1 : prevState.currentYear,
    }));
  };

  // Function to handle previous month
  prevMonth = () => {
    this.setState((prevState) => ({
      currentMonth: prevState.currentMonth === 0 ? 11 : prevState.currentMonth - 1,
      currentYear: prevState.currentMonth === 0 ? prevState.currentYear - 1 : prevState.currentYear,
    }));
  };

  // Function to render the calendar days
  renderDays() {
    const { currentMonth, currentYear, todayDate, todayMonth, todayYear } = this.state;
    const daysInMonth = this.getDaysInMonth(currentMonth, currentYear);
    const firstDayOfMonth = new Date(currentYear, currentMonth, 1).getDay();

    const days = [];
    // Add empty cells for days of the week before the 1st day of the month
    for (let i = 0; i < firstDayOfMonth; i++) {
      days.push(<div key={`empty-${i}`} className="calendar-day empty"></div>);
    }
    // Add days of the month
    for (let day = 1; day <= daysInMonth; day++) {
      const isToday =
        day === todayDate && currentMonth === todayMonth && currentYear === todayYear;
      days.push(
        <div
          key={day}
          className={`calendar-day ${isToday ? 'today' : ''}`}
        >
          {day}
        </div>
      );
    }

    return days;
  }

  render() {
    const { currentMonth, currentYear } = this.state;
    const monthNames = [
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December'
    ];

    return (
      <div className="calendar">
        <div className="calendar-header">
          <button onClick={this.prevMonth} className="calendar-button">&lt;</button>
          <span>{monthNames[currentMonth]} {currentYear}</span>
          <button onClick={this.nextMonth} className="calendar-button">&gt;</button>
        </div>
        <div className="calendar-grid">
          {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day) => (
            <div key={day} className="calendar-day-name">{day}</div>
          ))}
          {this.renderDays()}
        </div>
      </div>
    );
  }
}

export default Calendar;
