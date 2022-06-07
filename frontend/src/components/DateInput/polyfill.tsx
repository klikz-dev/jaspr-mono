import DatePicker from 'react-datepicker';
import { DateTime } from 'luxon';
import 'react-datepicker/dist/react-datepicker.css';

type DateInputPolyfillProps = {
    value: string | null;
    onChange: (dateString: string | null) => void;
    className: string;
} & DatePicker;

const PolyfillDatePicker = ({ value, onChange, ...props }: DateInputPolyfillProps): JSX.Element => {
    const date = value ? DateTime.fromFormat(value, 'yyyy-MM-dd') : null;

    return (
        <DatePicker
            scrollableYearDropdown
            showYearDropdown
            yearDropdownItemNumber={100}
            isClearable
            selected={date ? date.toJSDate() : null}
            clearButtonTitle="Clear"
            maxDate={new Date(new Date().setFullYear(new Date().getFullYear() - 13))} // Min age for Jaspr is 13
            minDate={new Date(new Date().setFullYear(new Date().getFullYear() - 113))} // Max age for Jaspr is 113
            wrapperClassName={props.className}
            onChange={(value) =>
                onChange(value ? DateTime.fromJSDate(value).toFormat('yyyy-MM-dd') : null)
            }
            {...props}
        />
    );
};

export default PolyfillDatePicker;
