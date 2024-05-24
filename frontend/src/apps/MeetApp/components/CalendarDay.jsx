import React from 'react';
import { Col } from 'react-bootstrap';

const CalendarDay = ({ date, events }) => (
  <Col className="calendar_day">
    {date}
    {events.map(event => (
      <div key={event.id} className="event">
        {event.summary}
      </div>
    ))}
  </Col>
);

export default CalendarDay;
