export function formatDate(dateString: string): string {
    const date = dateString?.substring(0, dateString.indexOf('T')) || dateString; // Trim off timestamp part of the date if set
    const [year, month, day] = (date || '').split('-');
    if (year && month && day) {
        return `${month}/${day}/${year}`;
    } else {
        return '-';
    }
}

export function formatDateTime(dateString: string): string {
    const date = new Date(dateString);
    if (!date) {
        return '-';
    }
    return `${formatDate(dateString)} ${date
        .getHours()
        .toString()
        .padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
}

const exports = {
    formatDateTime,
    formatDate,
};

export default exports;
