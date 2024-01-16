import {useState, useRef, useEffect} from 'react';
import {
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  View,
  Button,
  TextInput,
  TouchableOpacity,
  Keyboard,
  KeyboardAvoidingView,
} from 'react-native';
import {WebView} from 'react-native-webview';
import {html} from '../../../Components/html';
import axios from 'axios';
import Header from '../../../Components/Header';
import {useRoute} from '@react-navigation/native';

const Fundamental = ({navigation}) => {
  const webviewRef = useRef(null);
  const route = useRoute();
  const mathText = route.params.mathText;
  console.log(mathText);
  const handleSubmit = data => {
    const getData = async () => {
      try {
        await axios
          .post('http://localhost:8081/Calculus/fundamental', {data}) //here
          // .post('http://10.238.30.185:8081/Calculus/fundamental', {data})
          .then(res => {
            if (res.data.message) {
              console.log(res.data.message);
            } else {
              console.log(res.data.result.length);

              if (res.data.result.length < 1000) {
                navigation.navigate('Fundamental SOL', {
                  data: res.data.result,
                  equation: res.data.equation,  
                  step: res.data.step,
                  img: res.data.img,
                });
                console.log(typeof res.data.result);
                console.log(res.data.result);
              } else {
                console.log(456);
              }
            }
          });
      } catch (error) {
        // navigation.navigate('TabNavigator');
        console.log(123);
      }
    };
    getData();
  };

  //  useEffect(() => {
  //    handleButtonClick();
  //  }, []);

  function onMessage(data) {
    console.log('log o day', data.nativeEvent.data);
    handleSubmit(data.nativeEvent.data);
  }

  const handleButtonClick = () => {
    if (mathText !== null) {
      webviewRef.current.injectJavaScript(
        `changeData(${JSON.stringify(mathText)});`,
      );
    }
  };

  return (
    <SafeAreaView style={{flex: 1}}>
      <Header nav={'CalculusList'} />
      {mathText !== '' && (
        <Button onPress={handleButtonClick} title="Edit Equation" />
      )}
      <WebView
        ref={webviewRef}
        style={{flex: 1, padding: 0, margin: 0}}
        scalesPageToFit={false}
        bounces={false}
        scrollEnabled={false}
        mixedContentMode="compatibility"
        onMessage={onMessage}
        onError={() => console.log('Something went wrong')}
        source={{
          html: html,
        }}
      />
    </SafeAreaView>
  );
};

export default Fundamental;
