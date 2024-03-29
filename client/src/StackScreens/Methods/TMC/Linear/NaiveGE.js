import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  TextInput,
} from 'react-native';
import {useState} from 'react';
import axios from 'axios';
import Header from '../../../../Components/Header';
import Template from '../../../../Components/Template';

const NaiveGE = ({navigation}) => {
  const handleSubmit = e => {
    e.preventDefault();
    const getData = async () => {
      try {
        await axios
          .post('http://localhost:8081/Linear/naivege', {input}) //For Flask server
          .then(res => {
            if (res.data.message) {
              setErrorMessage(res.data.message);
            } else {
              navigation.navigate('Naive Gauss Elimination SOL', {
                data: res.data,
              });
              setErrorMessage(null);
            }
          });
      } catch (error) {
        if (error.response.status === 500) {
          setErrorMessage('Please re-check the input fields');
        } else if (error.response.status === 404) {
          setErrorMessage('Your are disconnecting with network!');
        }
      }
    };
    getData();
  };
  const [input, setInput] = useState();
  const [result, setResult] = useState(null);
  const [modalVisible, setModalVisible] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const handleChange = text => {
    setInput(JSON.stringify(text));
  };
  return (
    // <>
    //   <Header />
    //   <View style={styles.container}>

    //   </View>
    // </>
    <Template>
      <Text style={styles.title}>NAIVE GAUSS ELIMINATION CALCULATOR</Text>
      <View style={styles.input}>
        <View style={styles.functionField}>
          <View style={styles.firstValue}>
            <Text style={styles.noteText}>
              Provide value of matrix seperated by spaces
            </Text>
            <TextInput
              multiline={true}
              numberOfLines={4}
              placeholder={'It should be 4x3 matrix'}
              onChangeText={text => handleChange(text)}
              style={styles.inputField}
            />
          </View>
        </View>
      </View>

      <TouchableOpacity style={styles.submitButton} onPress={handleSubmit}>
        <Text style={styles.submitText}>Calculate</Text>
      </TouchableOpacity>
      {/* {result && <Text>{JSON.stringify(result)}</Text>} */}
      <Text style={{fontFamily: 'Kanit-Medium', color: 'red', fontSize: 16}}>
        {errorMessage}
      </Text>
    </Template>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    margin: '5%',
  },
  title: {
    fontFamily: 'Candal-Regular',
    color: 'black',
    fontSize: 26,
  },
  input: {
    marginBottom: '5%',
    marginTop: '5%',
  },
  functionField: {
    // flex: 1,
  },
  inputField: {
    borderWidth: 3,
    borderColor: '#2874fc',
    borderRadius: 12,
    paddingLeft: 16,
    marginBottom: '5%',
    fontSize: 22,
    textAlignVertical: 'top',
  },
  noteText: {
    fontSize: 18,
    color: 'black',
    marginBottom: '1%',
  },

  submitButton: {
    height: 48,
    backgroundColor: '#2874fc',
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },

  submitText: {
    fontFamily: 'Candal-Regular',
    fontSize: 20,
    color: 'white',
  },
});

export default NaiveGE;
