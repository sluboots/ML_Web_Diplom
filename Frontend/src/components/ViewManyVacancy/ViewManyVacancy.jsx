import React, {Component} from "react";
import {
    chakra,
    Box,
    Image,
    Flex,
    useColorModeValue,
    Link,
    SimpleGrid, Button,
    useDisclosure,
    Collapse, ListItem, OrderedList,
} from "@chakra-ui/react";
import {Link as RouteLink} from "react-router-dom";
import axios from "axios";
import authHeader from "../../services/user.service";
import Header from "../Header/Header";

const base_url = 'http://127.0.0.1:7000/api/onevacancy/';


function Collapse_Button(id_link1)
{
    const { isOpen, onToggle } = useDisclosure()
    const [post, setPost] = React.useState(null);

    React.useEffect(() => {
        axios.get(base_url + id_link1.children).then((response) =>{
            setPost(response.data);
        })
    })
    console.log(id_link1.children)
    return (
        <Box
            mx="auto"
            px={8}
            py={4}
            rounded="lg"
            shadow="lg"
            bg={useColorModeValue("white", "gray.800")}
            maxW="2xl"
            minW = "2xl"
            minH= "1xl"
        >
            <Box mt={2}>
                <chakra.p
                    textAlign={'center'}
                    fontSize="2xl"
                    color={useColorModeValue("gray.700", "white")}
                    fontWeight="700"
                    _hover={{
                        color: useColorModeValue("gray.600", "gray.200"),
                        textDecor: "underline",
                    }}
                >
                    Управление вакансией
                </chakra.p>
                <Flex justifyContent="space-around" alignItems="center" mt={10} p='10px'>
                    <Button onClick={onToggle}
                            display={{ base: 'none', md: 'inline-flex' }}
                            fontSize={'sm'}
                            fontWeight={600}
                            color={'black'}
                            bg={'gray.400'}
                            _hover={{
                                bg: 'green.200',
                            }}
                    >Найти резюме</Button>
                    <Button
                        display={{ base: 'none', md: 'inline-flex' }}
                        fontSize={'sm'}
                        fontWeight={600}
                        color={'black'}
                        bg={'gray.400'}
                        _hover={{
                            bg: 'red.500',
                        }}>
                        <RouteLink to='/login'>
                            Удалить
                        </RouteLink>
                    </Button>
                </Flex>
            </Box>
            <Collapse in={isOpen} animateOpacity
                      p='10px'>
                <Box
                    p='55px'
                    color='white'
                    bg='grey.100'
                    rounded='md'
                    shadow='md'
                >
                    <OrderedList mt={2} color={useColorModeValue("gray.600", "gray.300")}>
                        <ListItem><a href={post.data[0]}>Ссылка 1</a></ListItem>
                        <ListItem><a href={post.data[1]}>Ссылка 2</a></ListItem>
                        <ListItem><a href={post.data[2]}>Ссылка 3</a></ListItem>
                        <ListItem><a href={post.data[3]}>Ссылка 4</a></ListItem>
                        <ListItem><a href={post.data[4]}>Ссылка 5</a></ListItem>
                    </OrderedList>
                </Box>
            </Collapse>
        </Box>
    )
}


class ViewVacancy extends Component {
    constructor(props) {
        super(props);

        this.state = {
            posts: []
        }
    }

    componentDidMount() {
        let user = JSON.parse(localStorage.getItem('key'));
        const post = {
            refresh: user['refresh'],
        };
        axios.post('http://127.0.0.1:7000/api/token/refresh/', post)
            .then(res => {
                if (res.data.access) {
                    localStorage.setItem('key_access', JSON.stringify(res.data));
                    console.log(res.data['access']);
                }
            })
            .catch(error => {
                console.log(error)
            })

        axios.get('http://127.0.0.1:7000/api/vacancy/', {headers: authHeader()})
            .then(response => {
                console.log(response)
                this.setState({posts: response.data})
            })
            .catch(error => {
                console.log(error)
            })

    }

    //bg={useColorModeValue("#F9FAFB", "gray.600")}
    //bg={useColorModeValue("white", "gray.800")}
    //color={useColorModeValue("gray.600", "gray.400")}
    render(){
        const { posts } = this.state
        const itemLimit = 3;
        return (
            <>
                <chakra.p
                    textAlign={'center'}
                    fontSize="2xl"
                    color={"gray.700"}
                    p={5}
                    bg={"#F9FAFB"}
                    fontWeight="700"
                    _hover={{
                        color: "gray.600",
                        textDecor: "underline",
                    }}
                >
                    Мои Вакансии
                </chakra.p>
                <SimpleGrid
                    columns={2}
                    spacing={10}
                    bg={"#F9FAFB"}
                    p={100}
                    pb={60}
                    mb={40}
                    height={'100%'}
                    w="full"
                    alignItems="center"
                    justifyContent="center">
                    {
                        posts.length ?
                            posts.map(post =>
                                <>
                                    <Box
                                        mx="auto"
                                        px={8}
                                        py={4}
                                        rounded="lg"
                                        shadow="lg"
                                        bg={"white"}
                                        maxW="2xl"
                                    >
                                        <Flex justifyContent="space-between" alignItems="center">
                                            <chakra.span
                                                fontSize="sm"
                                                color={"gray.600"}
                                            >
                                                {post.created_at.slice(0, 10)}
                                            </chakra.span>
                                        </Flex>

                                        <Box mt={2}>
                                            <chakra.p mt={2} color={"gray.600"}>
                                                {post.resume.slice(0, 350)}
                                            </chakra.p>
                                        </Box>
                                    </Box>
                                    <Collapse_Button>{post.id}</Collapse_Button>
                                </>
                        ) :
                        null
                    }
                </SimpleGrid>
            </>

        );
    }
}

export default ViewVacancy;