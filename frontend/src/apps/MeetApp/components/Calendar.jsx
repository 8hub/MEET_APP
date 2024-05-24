import React, { useState } from 'react';
import { Container, Row, Button } from 'react-bootstrap';
import CalendarDay from './CalendarDay'

const Calendar = () => {
  const [month, setMonth] = useState(new Date().getMonth());
  const [year, setYear] = useState(new Date().getFullYear());

  // Hardcoded event data for debugging purposes
  const events = [
    {
      id: 1,
      summary: 'Meeting with Bob',
      date: new Date(year, month, 5).toISOString(),
    },
    {
      id: 2,
      summary: 'Lunch with Alice',
      date: new Date(year, month, 12).toISOString(),
    },
    {
      id: 3,
      summary: 'Project Deadline',
      date: new Date(year, month, 20).toISOString(),
    },
  ];

  const daysInMonth = new Date(year, month + 1, 0).getDate();

  const renderDays = () => {
    let days = [];
    for (let i = 1; i <= daysInMonth; i++) {
      const dayEvents = events.filter(event => new Date(event.date).getDate() === i);
      days.push(<CalendarDay key={i} date={i} events={dayEvents} />);
    }
    return days;
  };

  return (
    <Container>
      <Row className="navigation">
        <Button onClick={() => setMonth(month === 0 ? 11 : month - 1)}>Previous</Button>
        <Button onClick={() => setMonth(month === 11 ? 0 : month + 1)}>Next</Button>
      </Row>
      <Row>{renderDays()}</Row>
    </Container>
  );
};

export default Calendar;
