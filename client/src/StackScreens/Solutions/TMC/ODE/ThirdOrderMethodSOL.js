import {
  StyleSheet,
  Text,
  View,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import {useState} from 'react';
import {useRoute} from '@react-navigation/native';
import {Table, TableWrapper, Row} from 'react-native-table-component';
import MathView, {MathText} from 'react-native-math-view';
import Header from '../../../../Components/Header';

const ThirdOrderMethodSOL = ({navigation}) => {
  const route = useRoute();
  const data = route.params.data;
  const h = route.params.h;
  const [step, setStep] = useState(false);

  const tableHead = ['i', 'k1', 'k2', 'k3', 'x', 'y_3rd'];
  const widthArr = [180, 180, 180, 180, 180, 180];

  const tableData = data.map(e => Object.values(e));

  return (
    <>
      <Header />
      <View style={styles.container}>
        <Text style={styles.title}>Result!!</Text>
        <ScrollView style={styles.tabField} horizontal={true}>
          <View>
            <Table borderStyle={{borderWidth: 1, borderColor: '#C1C0B9'}}>
              <Row
                data={tableHead}
                widthArr={widthArr}
                style={styles.header}
                textStyle={styles.textHeader}
              />
            </Table>
            <ScrollView style={styles.dataWrapper}>
              <Table borderStyle={{borderWidth: 1, borderColor: '#C1C0B9'}}>
                {tableData.map((rowData, index) => (
                  <Row
                    key={index}
                    data={rowData}
                    widthArr={widthArr}
                    style={[
                      styles.row,
                      index % 2 && {backgroundColor: '#F7F6E7'},
                    ]}
                    textStyle={styles.text}
                  />
                ))}
              </Table>
            </ScrollView>
          </View>
        </ScrollView>

        <View style={styles.stepField}>
          <TouchableOpacity onPress={() => setStep(!step)}>
            <Text style={styles.showStep}>Show step</Text>
          </TouchableOpacity>
          {step && data[1] && (
            <ScrollView style={styles.step_container}>
              <View style={styles.step1}>
                <Text style={styles.stepTitle}>
                  STEP 1: Calculate the k1, k2, k3:
                </Text>
                <MathView
                  config={{ex: 15}}
                  resizeMode="cover"
                  math={`k_{1} = f(x_{1}, y_{1}) = ${data[0].slope} `}
                  style={styles.size_larger}
                />
                <MathView
                  config={{ex: 15}}
                  resizeMode="cover"
                  math={`k_{2} = f(x_{1} + \\frac{1}{2}h, y_{1} + k_{1}h) = ${data[0].slope2} `}
                  style={styles.size_mediumm}
                />
                <MathView
                  config={{ex: 15}}
                  resizeMode="cover"
                  math={`k_{3} = f(x_{1} + h, y_{1} - k_{1}h + 2k_{2}h) = ${data[0].slope3} `}
                  style={styles.size_mediumm}
                />
              </View>

              <View style={styles.step2}>
                <Text style={styles.stepTitle}>
                  STEP 2: Calculate y value of the next iteration:
                </Text>
                <MathView
                  config={{ex: 15}}
                  resizeMode="cover"
                  math={`y_{2} = y_{1} + \\frac{1}{6}(k_{1}+4k_{2}+k_{3}) * h`}
                  style={styles.size_large}
                />
                <MathView
                  config={{ex: 15}}
                  resizeMode="cover"
                  math={`= ${data[0].y_3rd} + \\frac{1}{6}(${data[0].slope}+4*${data[0].slope2}+${data[0].slope3})* ${h}`}
                  style={styles.size_small}
                />
                <MathView
                  config={{ex: 15}}
                  resizeMode="cover"
                  math={`Therefore: y_{2} = ${data[1].y_3rd}`}
                  style={styles.size_larger}
                />
              </View>
            </ScrollView>
          )}
        </View>
      </View>
    </>
  );
};

export default ThirdOrderMethodSOL;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    paddingTop: 30,
    backgroundColor: '#fff',
  },
  title: {
    fontFamily: 'Candal-Regular',
    fontSize: 28,
    color: '#2874fc',
  },
  tabField: {
    flex: 0.3,
  },
  stepField: {
    flex: 0.7,
  },
  header: {
    height: 50,
    backgroundColor: '#2874fc',
  },
  text: {
    textAlign: 'center',
    fontWeight: '500',
  },
  textHeader: {
    textAlign: 'center',
    fontWeight: '500',
    fontSize: 16,
    color: '#fff',
  },
  dataWrapper: {
    marginTop: -1,
  },
  row: {
    height: 40,
    backgroundColor: '#E7E6E1',
  },
  showStep: {
    marginTop: '5%',
    fontSize: 24,
    color: '#2874fc',
    textDecorationLine: 'underline',
    fontWeight: '700',
  },
  step_container: {
    marginTop: '3%',
  },
  stepTitle: {
    fontFamily: 'Candal-Regular',
    fontSize: 20,
    color: 'black',
  },
  size_medium: {
    width: '85%',
  },
  size_mediumm: {
    width: '75%',
  },
  size_large: {
    width: '65%',
  },
  size_larger: {
    width: '60%',
  },
});
