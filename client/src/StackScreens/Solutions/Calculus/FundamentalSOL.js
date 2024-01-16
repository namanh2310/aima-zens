import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  Image,
  Modal,
  ActivityIndicator,
} from 'react-native';
import {ScrollView} from 'react-native-gesture-handler';
import {useState} from 'react';
import {useRoute} from '@react-navigation/native';
import MathView, {MathText} from 'react-native-math-view';
import axios from 'axios';
import Header from '../../../Components/Header';
import {FontAwesomeIcon} from '@fortawesome/react-native-fontawesome';
import {faCodeCommit, faPencil} from '@fortawesome/free-solid-svg-icons';

const Fundamental = ({navigation}) => {
  const [show, setShow] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [options, setOptions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const route = useRoute();
  const scanImg = route.params.scanImg;
  const result = route.params.data;
  const equation = route.params.equation;
  const step = route.params.step;
  const img = route.params.img;

  console.log(result);
  console.log(equation);
  console.log(step);

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
              navigation.navigate('ReFundamental SOL', {
                data: res.data.result,
                equation: res.data.equation,
                step: res.data.step,
                img: res.data.img,
              });
            }
          });
      } catch (error) {
        navigation.navigate('TabNavigator');
      }
    };
    getData();
  };

  const regenerateScanResult = data => {
    setIsLoading(true);
    const getData = async () => {
      try {
        await axios
          .post('http://localhost:8081/AIScanner/AIforApp', {
            regenerate_status: true,
            img: scanImg,
          }) //here
          .then(res => {
            console.log(res.data);
            setModalVisible(true);
            setOptions(res.data.res_list);
            console.log(JSON.stringify(res.data.res_list));
          });
      } catch (error) {
        navigation.navigate('TabNavigator');
      } finally {
        setIsLoading(false);
      }
    };
    getData();
  };

  const editEquation = mathText => {
    navigation.navigate('Fundamental', {mathText});
  };

  const CustomModal = () => {
    return (
      <Modal
        animationType="slide"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => setModalVisible(false)}>
        <View style={styles.modalOverlay}>
          <View style={styles.modalView}>
            <Text style={styles.modalText}>OPTIONS</Text>
            {options.map(el => (
              <View style={styles.optionsContainer}>
                <TouchableOpacity onPress={() => handleSubmit(el)}>
                  <MathText
                    style={styles.mathText}
                    value={`\\(${el} \\)`}
                    direction="ltr"
                  />
                </TouchableOpacity>
                <TouchableOpacity onPress={() => editEquation(el)}>
                  <FontAwesomeIcon
                    icon={faPencil}
                    color={'#000'}
                    size={16}
                    style={styles.optionIcon}
                  />
                </TouchableOpacity>
              </View>
            ))}
            <TouchableOpacity
              style={styles.modalButton}
              onPress={() => setModalVisible(!modalVisible)}>
              <Text>Hide Modal</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    );
  };

  if (equation === undefined) {
    return (
      <>
        <Header />
        <View style={styles.container}>
          <View style={styles.infor}>
            <Text style={styles.textError}>
              Sorry, your inputted equation can not be read, please regenerate
              or scan again!
            </Text>
            <TouchableOpacity
              style={styles.showStepBtn}
              onPress={regenerateScanResult}>
              <Text style={styles.textBtn}>Re-generate</Text>
            </TouchableOpacity>
          </View>
        </View>
        <CustomModal />
      </>
    );
  }

  function IntegralEquation() {
    return (
      <>
        <Text
          style={{
            color: 'black',
            fontSize: 22,
            fontFamily: 'Kanit-Regular',
          }}>
          The problem is:
        </Text>

        <MathText
          style={styles.mathText}
          value={`\\(${equation} \\)`}
          direction="ltr"
        />

        {step.map(el => (
          <>
            <Text
              style={{
                color: 'black',
                fontSize: 22,
                fontFamily: 'Kanit-Regular',
              }}>
              Calculate the anti-derivative:
            </Text>
            <MathText
              style={styles.mathText}
              value={`\\( ${el[0]} \\) $$= \\(${el[1]} \\)`}
              direction="ltr"
            />

            <Text
              style={{
                color: 'black',
                fontSize: 22,
                fontFamily: 'Kanit-Regular',
              }}>
              Subtitute the range value to x, and then we can get the result
              Therefore, we get the value
            </Text>
            <MathText
              style={styles.mathText}
              value={`\\( ${el[2]} \\)`}
              direction="ltr"
            />
          </>
        ))}
      </>
    );
  }

  function UnstepEquation() {
    return (
      <>
        <Text
          style={{
            color: 'black',
            fontSize: 22,
            fontFamily: 'Kanit-Regular',
            marginBottom: '15%',
          }}>
          Updating soon . . .
        </Text>
      </>
    );
  }

  function StepEquation() {
    return (
      <>
        {step.map(el => (
          <MathText style={styles.mathText} value={el} direction="ltr" />
        ))}
      </>
    );
  }
  function BasicCalc() {
    return (
      <>
        <Text
          style={{
            color: 'black',
            fontSize: 18,
            fontFamily: 'Kanit-Regular',
          }}>
          The problem is
        </Text>
        <MathText value={` \\(${equation} \\)`} direction="ltr" />
        <Text
          style={{
            color: 'black',
            fontSize: 18,
            fontFamily: 'Kanit-Regular',
          }}>
          Do the basic calculation with operators, we have
        </Text>
        <MathText value={`\\(${equation} = ${result} \\)`} direction="ltr" />
      </>
    );
  }

  return (
    <>
      <Header content={'Calculus'} />

      <View style={styles.container}>
        {isLoading && (
          <View style={styles.loadingContainer}>
            {/* <Text style={styles.loadingText}>Loading . . .</Text> */}
            <ActivityIndicator size="large" color="red" />
          </View>
        )}
        <View style={styles.infor}>
          <MathView
            style={styles.equation}
            resizeMode="cover"
            math={equation}
          />
          <MathView
            style={
              typeof result === 'string' && result.length <= 40
                ? styles.result
                : typeof result === 'object' && result.length >= 4
                ? styles.result_scale
                : typeof result === 'string' && result.length >= 40
                ? styles.result_scale
                : styles.result
            }
            resizeMode="cover"
            math={typeof result !== 'string' ? result.toString() : result}
          />
          <TouchableOpacity
            style={styles.showStepBtn}
            onPress={regenerateScanResult}>
            <Text onPress={regenerateScanResult} style={styles.textBtn}>
              Re-generate
            </Text>
          </TouchableOpacity>
        </View>

        <View style={styles.step}>
          <ScrollView style={{marginHorizontal: '5%'}}>
            <Text
              style={{
                color: '#8252E7',
                fontSize: 22,
                fontFamily: 'Kanit-Regular',
                fontWeight: 800,
                marginVertical: '5%',
              }}>
              Here is the steps
            </Text>
            {step !== null && step.length !== 0 && equation.includes('int') ? (
              <IntegralEquation />
            ) : (
              <>
                {equation.includes('x') &&
                equation.includes('=') &&
                step.length === 1 ? (
                  <UnstepEquation />
                ) : (
                  <>
                    {equation.includes('x') && equation.includes('=') ? (
                      <StepEquation />
                    ) : (
                      <BasicCalc />
                    )}
                  </>
                )}
              </>
            )}
            {img && (
              <Image
                source={{uri: img}}
                style={{width: '100%', height: undefined, aspectRatio: 1.5}}
              />
            )}
          </ScrollView>
        </View>
      </View>
      <CustomModal />
    </>
  );
};

export default Fundamental;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  loadingContainer: {
    position: 'absolute',
    left: 0,
    right: 0,
    top: 0,
    bottom: 0,
    elevation: 3, // works on android
    alignItems: 'center',
    justifyContent: 'center',
  },
  optionsContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    width: '70%',
  },
  infor: {
    flex: 0.3,
    backgroundColor: '#8252E7',
    justifyContent: 'center',
    alignItems: 'flex-start',
    paddingTop: '5%',
    paddingLeft: '5%',
    paddingRight: '5%',
    paddingBottom: '10%',
    borderBottomLeftRadius: 22,
    borderBottomRightRadius: 22,
    width: '100%',
  },
  equation: {
    marginBottom: '5%',
    marginTop: '5%',
    color: '#fff',
    maxWidth: '100%',
  },
  result: {
    marginBottom: '5%',
    marginTop: '5%',
    color: '#fff',
  },

  result_scale: {
    width: '100%',
    marginBottom: '5%',
    marginTop: '5%',
    color: '#fff',
  },

  text: {
    fontSize: 24,
    fontWeight: 600,
    color: '#fff',
  },
  textError: {
    fontSize: 24,
    fontWeight: 600,
    color: '#fff',
    marginBottom: '15%',
  },
  showStepBtn: {
    width: '100%',
    height: 40,
    backgroundColor: '#fff',
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 12,
  },
  textBtn: {
    fontSize: 18,
    color: '#000',
    fontWeight: 500,
  },
  step: {
    flex: 0.7,
  },
  stepText: {
    fontSize: 20,
    color: 'black',
    marginTop: '5%',
  },
  stepTitle: {
    fontFamily: 'Candal-Regular',
    fontSize: 20,
    color: 'black',
  },
  mathText: {
    marginLeft: '3%',
  },
  modalOverlay: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.5)', // Semi-transparent background
  },
  modalView: {
    width: '90%',
    margin: 20,
    backgroundColor: 'white',
    borderRadius: 20,
    padding: 35,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5,
  },
});
