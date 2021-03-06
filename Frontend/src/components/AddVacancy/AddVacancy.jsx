import React from "react";
import {
    chakra,
    Box,
    Flex,
    useColorModeValue,
    SimpleGrid,
    GridItem,
    Heading,
    Text,
    Stack,
    FormControl,
    FormLabel,
    Input,
    InputGroup,
    InputLeftAddon,
    FormHelperText,
    Textarea,
    Avatar,
    Icon,
    Button,
    VisuallyHidden,
    Select,
    Checkbox,
    RadioGroup,
    Radio,
} from "@chakra-ui/react";
import { FaUser } from "react-icons/fa";
import {Link as RouteLink} from "react-router-dom";
import {Component} from "react";
import axios from "axios";
import authHeader from "../../services/user.service";

export default class AddVacancy extends Component {
    constructor(props) {
        super(props);
        this.state = {
            resume: ''
        }
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);

    };

    handleChange = event => {
        this.setState({resume: event.target.value});
        console.log(authHeader())
    }

    handleSubmit = event => {
        event.preventDefault();

        //let headers = { 'content-type': 'multipart/form-data'}
        const post = {
            resume: this.state.resume,
        };
        const json = JSON.stringify({resume: this.state.resume})
        axios.post(`http://127.0.0.1:7000/api/addvacancy/`, post, {headers: authHeader()})
            .then(res => {
                console.log(res);
                console.log(res.data);
                window.location.assign('/viewmanyvacancy')
            })
            .catch((error) => {
                console.log(error);
            })
    }
    render(){
        return(<Box bg={"gray.50"} p={10} pb={79}>
            <Box>
                <SimpleGrid
                    display={{ base: "initial", md: "grid" }}
                    columns={{ md: 3 }}
                    spacing={{ md: 6 }}
                >
                    <GridItem colSpan={{ md: 1 }}>
                        <Box px={[4, 0]}>
                            <Heading fontSize="lg" fontWeight="lg" lineHeight="6" color={"black"}>
                                ???????????????????? ????????????????
                            </Heading>
                            <Text
                                mt={1}
                                fontSize="sm"
                                color={"gray.600"}
                            >
                                ?????????? ???????????????? ????????????????, ???????????????????? ???????????? ?????????????????????? ?????? ???????????????? ?????????? ?? ???????? ?????? ??????????.
                                <br></br>
                                ???????????? ????????????????????:
                                <br></br>
                                ???????????????? ???????????? ???????? ???????????? ???? ?????????????? ??????????, ??????????????????????, ???? ???????????????????? ??????????, ???????????????? ??????????????????, ?? ?????????? ?????????????????? ????????????????????????.
                                <br></br>
                                ?????????????????????? ???????????????????? ???????????? ?????????? ????????????????.
                                <br></br>
                            </Text>
                        </Box>
                    </GridItem>
                    <GridItem mt={[5, null, 0]} colSpan={{ md: 2 }} maxW={'6xl'}>
                        <chakra.form
                            method="POST"
                            shadow="base"
                            rounded={[null, "md"]}
                            overflow={{ sm: "hidden" }}
                        >
                            <Stack
                                px={4}
                                py={5}
                                bg={"white"}
                                spacing={6}
                                p={{ sm: 6 }}
                            >
                                <div>
                                    <form onSubmit={this.handleSubmit}>
                                        <FormControl id="username" mt={1}>
                                            <FormLabel
                                                fontSize="sm"
                                                fontWeight="md"
                                                size="lg"
                                                color={"gray.700"}
                                            >
                                            </FormLabel>
                                            <Textarea
                                                placeholder="???????? ?????? ??????????"
                                                mt={1}
                                                rows={3}
                                                size="lg"
                                                height={490}
                                                shadow="sm"
                                                focusBorderColor="brand.400"
                                                color={"gray.700"}
                                                fontSize={{ sm: "sm" }}
                                                onChange={this.handleChange}
                                            />

                                        </FormControl>
                                    </form>

                                </div>
                            </Stack>
                            <Box
                                px={{ base: 4, sm: 6 }}
                                py={3}
                                bg={"gray.50"}
                                textAlign="right"
                            >
                                <Button
                                    display={{ base: 'none', md: 'inline-flex' }}
                                    fontSize={'sm'}
                                    fontWeight={600}
                                    color={'black'}
                                    bg={'gray.400'}
                                    _hover={{
                                        bg: 'red.100',
                                    }}
                                    onClick={(e) => this.handleSubmit(e)}

                                    >
                                    ????????????????
                                </Button>
                            </Box>
                        </chakra.form>
                    </GridItem>
                </SimpleGrid>
            </Box>
        </Box>);
    }
}
