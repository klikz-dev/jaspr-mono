import { lazy, Suspense } from 'react';

const dateInputSupported = (): boolean => {
    const i = document.createElement('input');
    i.setAttribute('type', 'date');
    return i.type !== 'text';
};

let DatePicker: any;
if (!dateInputSupported()) {
    DatePicker = lazy(() => import('./polyfill'));
}

interface DateInputProps {
    className?: string;
    value: string | null;
    onChange: (dateString: string | null) => void;
    required?: boolean;
    pattern?: string;
}

const DateInput = ({
    className = '',
    value,
    onChange = () => {},
    required = false,
    pattern,
}: DateInputProps): JSX.Element => {
    const handleChange = (dateString: string) => {
        onChange(dateString);
    };

    if (DatePicker) {
        return (
            <Suspense fallback="loading...">
                <DatePicker
                    pattern={pattern}
                    className={className}
                    onChange={handleChange}
                    placeholder="MM/DD/YYYY"
                    value={value}
                    required={required}
                />
            </Suspense>
        );
    } else {
        return (
            <input
                pattern={pattern}
                className={className}
                type="date"
                placeholder="MM/DD/YYYY"
                value={value}
                required={required}
                onChange={({ target }) => handleChange(target.value)}
            />
        );
    }
};

export { DateInput };
export default DateInput;
