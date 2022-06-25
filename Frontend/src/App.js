import Header from './components/Header/Header';
import Login from "./components/Login/Login";
import Homepage from "./components/Main/Main_Section";
import SmallCentered from "./components/Footer/Footer";
import AddVacancy from "./components/AddVacancy/AddVacancy";
import AddResume from "./components/AddResume/AddResume";
import ViewVacancy from "./components/ViewManyVacancy/ViewManyVacancy";
import ViewResume from "./components/ViewManyResume/ViewManyResume";
import Register from "./components/Register/Register";
import AppFooter from "./components/Footer/Footer";

import { Route, Switch} from "react-router-dom";
import { ChakraProvider, extendTheme} from '@chakra-ui/react'
import { BrowserRouter as Router } from "react-router-dom";
import { mode } from '@chakra-ui/theme-tools';


function App() {
    return (
        <ChakraProvider theme={extendTheme({
            styles: {
                global: (props) => ({
                    body: {
                        bg: mode('white')(props),
                        color: mode('white')(props),
                    },
                }),
            },
        })}>
            <Router>
                <Header></Header>
                <Switch>
                    <Route path="/login" component={Login}></Route>
                    <Route path="/register" component={Register}></Route>
                    <Route path="/homepage">
                        <Homepage/>
                        <SmallCentered></SmallCentered>
                    </Route>
                    <Router path="/addvacancy">
                        <AddVacancy/>
                        <SmallCentered></SmallCentered>
                    </Router>
                    <Router path="/addresume">
                        <AddResume/>
                        <SmallCentered></SmallCentered>
                    </Router>
                    <Router path="/viewmanyvacancy">
                        <ViewVacancy/>
                    </Router>
                    <Router path="/viewmanyresume">
                        <ViewResume/>
                    </Router>

                </Switch>
            </Router>
        </ChakraProvider>
    );
}

export default App;
