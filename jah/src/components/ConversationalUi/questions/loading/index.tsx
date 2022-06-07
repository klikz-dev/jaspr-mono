import React, { useEffect, useRef } from 'react';
import { Animated } from 'react-native';
import Styled from 'styled-components/native';
import styles from './index.module.scss';

const Container = Styled.View`${styles.loading} margin-left: 18px;`;
const Dot = Styled.View`
    display: flex;
    width: 12px;
    height: 12px;
    border-radius: 6px;
    background-color: rgb(159, 157, 157);
    margin: 0 3px;
`;

const AnimatedDot = Animated.createAnimatedComponent(Dot);

const Loading = (): JSX.Element => {
    const timing = useRef(new Animated.Value(0)).current;

    useEffect(() => {
        const animate = () => {
            Animated.loop(
                Animated.timing(timing, {
                    toValue: 4,
                    useNativeDriver: true,
                    duration: 1500,
                }),
            ).start();
        };
        animate();
    }, [timing]);

    return (
        <Container>
            <AnimatedDot
                style={{
                    transform: [
                        {
                            scale: timing.interpolate({
                                inputRange: [0, 1, 2, 3, 4],
                                outputRange: [1, 1.3, 1, 1, 1],
                            }),
                        },
                    ],
                    opacity: timing.interpolate({
                        inputRange: [0, 1, 2, 3, 4],
                        outputRange: [0.5, 1, 1, 0.5, 0.5],
                    }),
                }}
            />
            <AnimatedDot
                style={{
                    transform: [
                        {
                            scale: timing.interpolate({
                                inputRange: [0, 1, 2, 3, 4],
                                outputRange: [1, 1, 1.3, 1, 1],
                            }),
                        },
                    ],
                    opacity: timing.interpolate({
                        inputRange: [0, 1, 2, 3, 4],
                        outputRange: [0.5, 1, 1, 0.5, 0.5],
                    }),
                }}
            />
            <AnimatedDot
                style={{
                    transform: [
                        {
                            scale: timing.interpolate({
                                inputRange: [0, 1, 2, 3, 4],
                                outputRange: [1, 1, 1, 1.3, 1],
                            }),
                        },
                    ],
                    opacity: timing.interpolate({
                        inputRange: [0, 1, 2, 3, 4],
                        outputRange: [0.5, 0.5, 1, 1, 0.5],
                    }),
                }}
            />
        </Container>
    );
};

export default Loading;
