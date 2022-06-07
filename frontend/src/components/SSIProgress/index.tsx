interface Props {
    progress: 0 | 1 | 2 | 3;
}

const SSIProgress = ({ progress = 0 }: Props) => {
    return (
        <svg width="34px" height="34px" viewBox="0 0 34 34" version="1.1">
            <g fill="none">
                <circle stroke="#DADADA" strokeWidth="7" cx="17" cy="17" r="13" />
                {progress > 0 && (
                    <path
                        d='M33.0715491,8.61169224 C31.2422022,7.62900588 29.1504271,7.07154908 26.9284509,7.07154908 C21.9840142,7.07154908 17.6842946,9.83191137 15.486271,13.8956571 C14.4925956,15.7327821 13.9284509,17.8362841 13.9284509,20.0715491" stroke="#6CC5D4" stroke-width="7" transform="translate(23.500000, 13.571549) rotate(-270.000000) translate(-23.500000, -13.571549)'
                        stroke="#6CC5D4"
                        stroke-width="7"
                        transform="translate(23.500000, 13.571549) rotate(-270.000000) translate(-23.500000, -13.571549) "
                    />
                )}
                {progress > 1 && (
                    <path
                        d="M24.3772628,29.1286923 C25.5945929,28.4236438 26.6869865,27.5268071 27.6131117,26.4795142 C29.6406729,24.1866813 30.8713077,21.1727096 30.8713077,17.8713077 C30.8713077,10.691606 25.0510095,4.87130774 17.8713077,4.87130774 C12.926871,4.87130774 8.62715139,7.63167002 6.42912779,11.6954158 C5.43545238,13.5325408 4.87130774,15.6360427 4.87130774,17.8713077"
                        stroke="#6CC5D4"
                        strokeWidth="7"
                        transform="translate(17.871308, 17.000000) rotate(-270.000000) translate(-17.871308, -17.000000) "
                    />
                )}
                {progress > 2 && (
                    <circle stroke="#6CC5D4" stroke-width="7" cx="17" cy="17" r="13"></circle>
                )}
                <line stroke="#FFFFFF" x1="17" y1="0" x2="17" y2="8" strokeWidth="2" />
                <line stroke="#FFFFFF" x1="31" y1="26" x2="25" y2="22" strokeWidth="2" />
                <line stroke="#FFFFFF" x1="3" y1="26" x2="9" y2="22" strokeWidth="2" />
            </g>
        </svg>
    );
};

export { SSIProgress };
export default SSIProgress;
