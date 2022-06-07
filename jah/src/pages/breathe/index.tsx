import React, { useCallback, useEffect, useState, useRef } from 'react';
import { Animated, Dimensions, Easing, ImageBackground, Modal, SafeAreaView } from 'react-native';
import Styled from 'styled-components/native';
import { Svg, G, Circle, Text as SVGText, Line } from 'react-native-svg';
import styles from './index.module.scss';
import background from './background.png';
import { useHistory } from 'lib/router';

const AnimatedCircle = Animated.createAnimatedComponent(Circle);
const AnimatedText = Animated.createAnimatedComponent(SVGText);
const AnimatedG = Animated.createAnimatedComponent(G);
const StepText = Styled.Text`
    color: #fff;
    font-size: 20px;
    margin-top: auto;
    margin-bottom: auto;
`;
const StartButton = Styled.TouchableOpacity`
    height: 49px;
    width: 155px;
    border-radius: 4px;
    margin-top: auto;
    margin-bottom: 55px;
    border-color: #77ddf1;
    border-width: 1px;
    align-items: center;
    justify-content: center;
`;
const ButtonText = Styled.Text`
    color: white;
    font-size: 22px;
`;
const CloseButton = Styled.TouchableOpacity`
    margin-left: auto;
    width: 34px;
    height: 34px;
`;
const CloseText = Styled.Text`
    color: #fff;
    font-weight: bold;
    font-size: 30px;
`;

const BpmButton = Styled.TouchableOpacity`
    position: absolute;
    right: 0;
    bottom: 0;
    height: 43px;
    width: 115px;
    backgroundColor: rgba(119,221,241,.8);
    color: #fff;
    align-items: center;
    justify-content: center;
`;
const BpmButtonText = Styled.Text`color: #fff; font-size: 18px;`;
const BpmContainer = Styled.View`width: 80%; backgroundColor: #fff;align-self: center; marginTop: auto; marginBottom: auto; border-radius: 5px; padding-vertical: 10px;`;
const BpmItem = Styled.TouchableOpacity`margin-vertical: 10px; padding-horizontal: 10px;`;
const BpmText = Styled.Text``;

const getDot = (radius: number, dots: number, number: number) => {
    const angle = (number / (dots / 2)) * Math.PI;
    const width = radius * 2 + 30;
    const height = radius * 2 + 30;
    const x = radius * Math.cos(angle) + width / 2;
    const y = radius * Math.sin(angle) + height / 2;
    return (
        <Circle key={`${radius}-${number}`} cx={x} cy={y} r="2.5" fill="rgba(255,255,255,0.8)" />
    );
};

const Breathe = () => {
    const history = useHistory();
    const INITIAL_BREATHS = 5;
    const [playing, setPlaying] = useState(false);
    const [remainingBreaths, setRemainingBreaths] = useState(INITIAL_BREATHS);
    const [totalBreaths, setTotalBreaths] = useState(0);
    const [bpm, setBpm] = useState({
        label: '6 BPM',
        value: '6',
    });
    const { width, height } = Dimensions.get('window');
    const [bpmOpen, setBpmOpen] = useState(false);
    const rotation = useRef(new Animated.Value(0)).current;
    const innerRadius = useRef(new Animated.Value(0)).current;
    const textTiming = useRef(new Animated.Value(0)).current;
    const radius = Math.min(width / 2 - 30, height / 2 - 30, 200); // The smaller of width, height or a set max size of 200
    const dots = Math.floor(radius / 3);
    const svgWidth = radius * 2 + 30;
    const svgHeight = radius * 2 + 30;

    const togglePlay = () => {
        if (!playing) {
            requestAnimationFrame(() => setPlaying(true));
        } else {
            setPlaying(false);
        }
    };

    const startAnimation = useCallback(() => {
        rotation.setValue(0);
        innerRadius.setValue(0);
        textTiming.setValue(0);

        const sequence1Time = ((60 / parseInt(bpm.value, 10)) * 1000 * 3) / 10;
        const sequence2Time = ((60 / parseInt(bpm.value, 10)) * 1000 * 2) / 10;
        const sequence3Time = ((60 / parseInt(bpm.value, 10)) * 1000 * 5) / 10;

        Animated.parallel([
            Animated.sequence([
                Animated.timing(textTiming, {
                    toValue: 1,
                    useNativeDriver: true,
                    easing: Easing.step1,
                    duration: sequence1Time,
                }),
                Animated.timing(textTiming, {
                    toValue: 2,
                    useNativeDriver: true,
                    easing: Easing.step1,
                    duration: sequence2Time,
                }),
                Animated.timing(textTiming, {
                    toValue: 3,
                    useNativeDriver: true,
                    easing: Easing.step1,
                    duration: sequence3Time,
                }),
            ]),
            Animated.timing(rotation, {
                toValue: 1,
                useNativeDriver: true,
                easing: Easing.linear,
                duration: sequence1Time + sequence2Time + sequence3Time,
                isInteraction: false,
            }),
            Animated.sequence([
                Animated.timing(innerRadius, {
                    toValue: 1,
                    useNativeDriver: true,
                    duration: sequence1Time,
                }),
                Animated.timing(innerRadius, {
                    toValue: 1,
                    useNativeDriver: true,
                    duration: sequence2Time,
                }),
                Animated.timing(innerRadius, {
                    toValue: 0,
                    useNativeDriver: true,
                    duration: sequence3Time,
                }),
            ]),
        ]).start(({ finished }) => {
            if (finished) {
                startAnimation();
                setTotalBreaths((prevBreaths) => prevBreaths + 1);
            }
        });
    }, [bpm.value, textTiming, innerRadius, rotation, setTotalBreaths]);

    const stopAnimation = useCallback(() => {
        // TODO Check config arg works correctly
        Animated.timing(innerRadius, { toValue: 0, useNativeDriver: true }).stop();
        Animated.timing(rotation, { toValue: 0, useNativeDriver: true }).stop();
    }, [innerRadius, rotation]);

    const opacityInhale = textTiming.interpolate({
        inputRange: [0, 1, 2],
        outputRange: [1, 0, 0],
    });
    const opacityHold = textTiming.interpolate({
        inputRange: [0, 1, 2],
        outputRange: [0, 1, 0],
    });
    const opacityExhale = textTiming.interpolate({
        inputRange: [0, 1, 2],
        outputRange: [0, 0, 1],
    });

    const changeBpm = (bpm: '2' | '3' | '4' | '5' | '6' | '7' | '8'): void => {
        setBpm({
            label: `${bpm} BPM`,
            value: bpm,
        });
        setBpmOpen(false);
    };

    useEffect(() => {
        if (playing && totalBreaths > 0 && INITIAL_BREATHS - totalBreaths >= 0) {
            setRemainingBreaths((prevBreaths) => prevBreaths - 1);
        }
    }, [playing, totalBreaths]);

    useEffect(() => {
        if (playing) {
            startAnimation();
        } else {
            stopAnimation();
            rotation.setValue(0);
        }
    }, [rotation, playing, startAnimation, stopAnimation]);

    useEffect(() => {
        rotation.setValue(0); // Sets the orbiter to the default position at load
    }, [rotation]);

    useEffect(() => {
        return stopAnimation; // Stop the animation before unmounting the component
    }, [stopAnimation]);

    useEffect(() => {
        if (playing) {
            stopAnimation();
            startAnimation();
        }
    }, [playing, bpm.value, stopAnimation, startAnimation]);
    return (
        <ImageBackground
            source={background}
            resizeMode="cover"
            style={{
                flex: 1,
                width: '100%',
                justifyContent: 'center',
                alignItems: 'center',
                opacity: 0.8,
            }}
        >
            <SafeAreaView />
            <CloseButton onPress={history.goBack}>
                <CloseText>⨉</CloseText>
            </CloseButton>
            {remainingBreaths === INITIAL_BREATHS && (
                <StepText>Let's start with {INITIAL_BREATHS} breaths.</StepText>
            )}
            {remainingBreaths > 0 && remainingBreaths < INITIAL_BREATHS && (
                <StepText>
                    {remainingBreaths} more breath{remainingBreaths > 1 ? 's' : ''}.
                </StepText>
            )}
            {remainingBreaths <= 0 && (
                <StepText>You've taken {totalBreaths} calming breaths.</StepText>
            )}

            <Svg width={svgWidth} height={svgHeight} viewBox={`0 0 ${svgWidth} ${svgHeight}`}>
                <G>
                    {[...Array(dots)].map((e, i) => getDot(radius, dots, i))}
                    <AnimatedCircle
                        x={radius + 15}
                        y={radius + 15}
                        cx={radius / 1.41}
                        cy={radius / 1.41} // TODO Magic number I don't understand
                        r={6}
                        fill="#fff"
                        // @ts-ignore
                        style={{
                            transform: [
                                {
                                    rotate: rotation.interpolate({
                                        inputRange: [0, 1],
                                        outputRange: ['-135deg', '225deg'],
                                    }),
                                },
                            ],
                        }}
                    />
                    <AnimatedCircle
                        cx={radius + 15}
                        cy={radius + 15}
                        fill="#68bbd0"
                        // @ts-ignore
                        style={{ mixBlendMode: 'soft-light', opacity: 0.75 }}
                        r={innerRadius.interpolate({
                            inputRange: [0, 1],
                            outputRange: ['60', `${Math.round(radius * 0.8)}`],
                        })}
                    />
                    <Line
                        x1={svgWidth / 2}
                        x2={svgWidth / 2}
                        y1={12}
                        y2={30}
                        strokeWidth="3"
                        stroke="rgba(104, 187, 208, 1)"
                    />
                    <Line
                        x1={radius * Math.cos(0.5) + (radius * 2 + 30) / 2}
                        x2={radius * Math.cos(0.5) + (radius * 2 + 30) / 2 - 15}
                        y1={radius * Math.sin(0.5) + (radius * 2 + 30) / 2}
                        y2={radius * Math.sin(0.5) + (radius * 2 + 30) / 2 - 8}
                        strokeWidth="3"
                        stroke="rgba(104, 187, 208, 1)"
                    />
                    <Line
                        x1={svgWidth / 2}
                        x2={svgWidth / 2}
                        y1={svgHeight - 12}
                        y2={svgHeight - 30}
                        strokeWidth="3"
                        stroke="rgba(104, 187, 208, 1)"
                    />
                </G>
                <G>
                    {!playing && (
                        <SVGText
                            fontWeight="bold"
                            fontSize="20"
                            x="50%"
                            y={svgHeight / 2 + 10}
                            textAnchor="middle"
                            fill="#fff"
                        >
                            Ready?
                        </SVGText>
                    )}
                    {playing && (
                        <>
                            <AnimatedG opacity={opacityInhale}>
                                <SVGText
                                    fontWeight="bold"
                                    fontSize="20"
                                    x="50%"
                                    y={svgHeight / 2 + 10}
                                    textAnchor="middle"
                                    fill="#fff"
                                >
                                    Inhale
                                </SVGText>
                            </AnimatedG>
                            <AnimatedG opacity={opacityHold}>
                                <AnimatedText
                                    fontWeight="bold"
                                    fontSize="20"
                                    fill="#fff"
                                    x="50%"
                                    y={svgHeight / 2 + 10}
                                    textAnchor="middle"
                                >
                                    Hold
                                </AnimatedText>
                            </AnimatedG>
                            <AnimatedG opacity={opacityExhale}>
                                <AnimatedText
                                    fontWeight="bold"
                                    fontSize="20"
                                    x="50%"
                                    y={svgHeight / 2 + 10}
                                    textAnchor="middle"
                                    fill="#fff"
                                >
                                    Exhale
                                </AnimatedText>
                            </AnimatedG>
                        </>
                    )}
                </G>
            </Svg>
            <Modal visible={bpmOpen} animationType="fade" transparent={true}>
                <BpmContainer>
                    <BpmItem onPress={() => changeBpm('2')}>
                        <BpmText>2 BPM</BpmText>
                    </BpmItem>
                    <BpmItem onPress={() => changeBpm('3')}>
                        <BpmText>3 BPM</BpmText>
                    </BpmItem>
                    <BpmItem onPress={() => changeBpm('4')}>
                        <BpmText>4 BPM</BpmText>
                    </BpmItem>
                    <BpmItem onPress={() => changeBpm('5')}>
                        <BpmText>5 BPM</BpmText>
                    </BpmItem>
                    <BpmItem onPress={() => changeBpm('6')}>
                        <BpmText>6 BPM</BpmText>
                    </BpmItem>
                    <BpmItem onPress={() => changeBpm('7')}>
                        <BpmText>7 BPM</BpmText>
                    </BpmItem>
                    <BpmItem onPress={() => changeBpm('8')}>
                        <BpmText>8 BPM</BpmText>
                    </BpmItem>
                </BpmContainer>
            </Modal>
            <BpmButton onPress={() => setBpmOpen(true)}>
                <BpmButtonText>{`${bpm.label} ▼`}</BpmButtonText>
            </BpmButton>
            <StartButton onPress={togglePlay}>
                <ButtonText>{playing ? 'Stop' : 'Start'}</ButtonText>
            </StartButton>
        </ImageBackground>
    );
};

export default Breathe;
