import { StyleSheet, ViewStyle, ImageStyle, TextStyle } from 'react-native';

const styles = StyleSheet.create({
    container: {
        display: 'flex',
        flexDirection: 'column',
        width: '100%',
        flexGrow: 1,
        justifyContent: 'center',
        backgroundColor: 'rgba(236, 238, 245, 1)',
    },
    button: {
        display: 'flex',
        marginTop: '25px',
        marginLeft: 'auto',
        marginRight: 'auto',
        height: '55px',
        width: '162px',
        borderRadius: 17,
        backgroundColor: 'rgba(92, 101, 151, 1)',
    },
    buttonText: {
        margin: 'auto',
        color: 'rgba(255, 255, 255, 1)',
        fontSize: 22,
        fontWeight: '500',
        letterSpacing: 0.17,
        textAlign: 'center',
    },
});

export default styles;
