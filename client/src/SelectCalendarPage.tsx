import { useEffect, useState, Fragment } from 'react';
import { FormControl, InputLabel, Select, MenuItem } from '@mui/material'
import axios from 'axios';
import './LoginPage.scss';

function SelectCalendarPage(props: {
  isLoggedIn: boolean,
  userInfo: string | any,
}) {
  const [calendarList, setCalendarList] = useState<{
    [id: string]: string
  }>({});
  const [selected, setSelected] = useState<string>('');

  useEffect(() => {
    if (props.isLoggedIn) {
      axios.get('/calendar-list').then((res) => {
        setCalendarList(res.data);
      });
    }
  }, []);
  
  return calendarList && props.isLoggedIn ? (
    <Fragment>
      <div >
        Welcome, {props.userInfo.name}!
      </div>
      <FormControl fullWidth>
        <InputLabel id="calendar-label">Calendar</InputLabel>
        <Select
          labelId="calendar-label"
          id="select-calendar"
          value={selected}
          label="Age"
          onChange={(event) => {
            setSelected(event.target.value);

            axios.post('/select-calendar', {
              calendarId: event.target.value,
            });
          }}
        >
          {Object.entries(calendarList).map(([id, name]) => {
            console.log(id, name);
            return (
              <MenuItem value={id}>{name}</MenuItem>
            );
          })}
        </Select>
      </FormControl>
    </Fragment>
  ) : null;
}

export default SelectCalendarPage;
