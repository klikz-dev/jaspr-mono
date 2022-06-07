import React from 'react';
import Svg, { Rect, Defs, LinearGradient, Stop } from 'react-native-svg';

const linear = (key: string) => {
    return [
        <Stop offset="0" stopColor={'#000'} stopOpacity={0.8} key={key + 'Linear0'} />,
        <Stop offset="1" stopColor={'#000'} stopOpacity="0" key={key + 'Linear1'} />,
    ];
};

const TopShadow = (): JSX.Element => {
    return (
        <Svg height={4} style={{ position: 'absolute', top: -4, width: '100%' }}>
            <Defs>
                <LinearGradient id="top" x1="0%" x2="0%" y1="100%" y2="0%">
                    {linear('BorderTop')}
                </LinearGradient>
            </Defs>
            <Rect x={0} y={0} width={'100%'} height={4} fill={`url(#top)`} />
        </Svg>
    );
};

export default TopShadow;
