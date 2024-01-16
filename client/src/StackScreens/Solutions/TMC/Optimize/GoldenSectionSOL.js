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

const GoldenSectionSOL = ({navigation}) => {
  const route = useRoute();
  const data = route.params.data;
  const [step, setStep] = useState(false);
  const comp = data[0].f1 > data[0].f2 ? '>' : '<';

  const tableHead = [
    'd',
    'ea(%)',
    'f(x1)',
    'f(x2)',
    'i',
    'x1',
    'x2',
    'xl',
    'xu',
  ];
  const widthArr = [120, 120, 120, 120, 120, 120, 120, 120, 120];

  const tableData = data.map(e => Object.values(e));

  return (
    <>
      <Header />
      <View style={styles.container}>
        <Text style={styles.title}>RESULT!</Text>
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
                <Text style={styles.stepTitle}>STEP 1: CALCULATE</Text>
                <MathView
                  resizeMode="cover"
                  math={`d = R(x_l - x_u) = \\frac{\\sqrt{5} - 1}{2} (${data[0].xu} - ${data[0].xl}) = ${data[0].d}`}
                />
                <MathView
                  resizeMode="cover"
                  math={`x_1 = x_l + d = ${data[0].xl} + ${data[0].d} = ${data[0].x1}`}
                  style={styles.size_medium}
                />
                <MathView
                  resizeMode="cover"
                  math={`x_2 = x_u - d = ${data[0].xu} - ${data[0].d} = ${data[0].x2}`}
                  style={styles.size_medium}
                />
              </View>

              <View style={styles.step2}>
                <Text style={styles.stepTitle}>STEP 2: CHECK</Text>
                <MathView
                  resizeMode="cover"
                  math={`f(x_1) = ${data[0].f1} ${comp} f(x_2) = ${data[0].f2}`}
                  style={styles.size_medium}
                />
                <MathView
                  resizeMode="cover"
                  math={`=> x_l = x_{opt} = x_2 = ${data[0].x2}`}
                  style={styles.size_large}
                />
              </View>

              <View style={styles.step3}>
                <Text style={styles.stepTitle}>STEP 3: Calculate error</Text>
                <MathView
                  resizeMode="cover"
                  math={`e_a = (1 - R) * \\frac{interval}{x_{opt}}*100`}
                  style={styles.size_large}
                />
                <MathView
                  resizeMode="cover"
                  math={`= (1 - \\frac{\\sqrt{5} - 1}{2})\\frac{${
                    data[0].xu - data[0].xl
                  }}{ ${data[0].x2}}*100=${data[0].ea}`}
                  style={styles.size_medium}
                />
              </View>
            </ScrollView>
          )}
        </View>
      </View>
    </>
  );
};

export default GoldenSectionSOL;

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
    flex: 0.5,
  },
  stepField: {
    flex: 0.5,
  },
  header: {
    height: 50,
    backgroundColor: '#2874fc',
  },
  textHeader: {
    textAlign: 'center',
    fontWeight: '500',
    fontSize: 16,
    color: '#fff',
  },
  text: {
    textAlign: 'center',
    fontWeight: '500',
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
  size_large: {
    width: '65%',
  },
  size_larger: {
    width: '60%',
  },
});
