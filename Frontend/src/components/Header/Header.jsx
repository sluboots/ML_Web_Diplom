import {
    Box,
    Flex,
    Text,
    IconButton,
    Button,
    Stack,
    Collapse,
    Icon,
    Link,
    Popover,
    PopoverTrigger,
    PopoverContent,
    useColorModeValue,
    useBreakpointValue,
    useDisclosure,
} from '@chakra-ui/react';
import {Link as RouteLink} from "react-router-dom";
import React, {Component} from "react";
import AuthService from "../../services/auth.service";
import {
    HamburgerIcon,
    CloseIcon,
    ChevronDownIcon,
    ChevronRightIcon,
} from '@chakra-ui/icons';

const DesktopNav = () => {
    const linkColor = useColorModeValue('gray.600', 'gray.600');
    const linkHoverColor = useColorModeValue('gray.800', 'gray.800');
    const popoverContentBgColor = useColorModeValue('white', 'white');

    return (
        <Stack direction={'row'} spacing={4}>
            {NAV_ITEMS.map((navItem) => (
                <Box key={navItem.label}>
                    <Popover trigger={'hover'} placement={'bottom-start'}>
                        <PopoverTrigger>
                            <Link
                                p={2}
                                fontSize={'sm'}
                                fontWeight={500}
                                color={linkColor}
                                _hover={{
                                    textDecoration: 'none',
                                    color: linkHoverColor,
                                }}>
                                {navItem.label}
                            </Link>
                        </PopoverTrigger>

                        {navItem.children && (
                            <PopoverContent
                                border={0}
                                boxShadow={'xl'}
                                bg={popoverContentBgColor}
                                p={4}
                                rounded={'xl'}
                                minW={'sm'}>
                                <Stack>
                                    {navItem.children.map((child) => (
                                        <DesktopSubNav key={child.label} {...child} />
                                    ))}
                                </Stack>
                            </PopoverContent>
                        )}
                    </Popover>
                </Box>
            ))}
        </Stack>
    );
};

const DesktopSubNav = ({ label, href, subLabel }: NavItem) => {
    return (
        <Link
            role={'group'}
            display={'block'}
            p={2}
            rounded={'md'}
            _hover={{ bg: useColorModeValue('red.100', 'red.100') }}>
            <Stack direction={'row'} align={'center'}>
                <Box>
                    <RouteLink to= {href}>
                        <Text
                            transition={'all .3s ease'}
                            _groupHover={{ color: 'white.400' }}
                            fontWeight={500}>
                            {label}

                        </Text>
                        <Text fontSize={'sm'}>{subLabel}</Text>
                    </RouteLink>

                </Box>
                <Flex
                    transition={'all .3s ease'}
                    transform={'translateX(-10px)'}
                    opacity={0}
                    _groupHover={{ opacity: '100%', transform: 'translateX(0)' }}
                    justify={'flex-end'}
                    align={'center'}
                    flex={1}>
                    <Icon color={'white.400'} w={5} h={5} as={ChevronRightIcon} />
                </Flex>
            </Stack>
        </Link>
    );
};


interface NavItem {
    label: string;
    subLabel?: string;
    children?: Array<NavItem>;
    href?: string;
}

const NAV_ITEMS: Array<NavItem> = [
    {
        label: 'Добавить',
        children: [
            {
                label: 'Вакансию',
                subLabel: 'Для поиска наиболее подходящих резюме',
                href: '/addvacancy',
            },
            {
                label: 'Резюме',
                subLabel: 'Для поиска наиболее подходящих вакансий',
                href: '/addresume',
            },
        ],
    },
    {
        label: 'Мои',
        children: [
            {
                label: 'Вакансии',
                subLabel: 'Посмотреть все Ваши добавленные вакансии',
                href: '/viewmanyvacancy',
            },
            {
                label: 'Резюме',
                subLabel: 'Посмотреть все Ваши добавленные резюме',
                href: '/viewmanyresume',
            },
        ],
    },
];

export default class Header extends Component {
    constructor(props) {
        super(props);
        this.logOut = this.logOut.bind(this);
        this.state = {
            currentUser: undefined,
        };
    }

    componentDidMount() {
        const user = AuthService.getCurrentUser();
        if(user) {
            this.setState({
                currentUser: user,
            });
        }
    }
    logOut(){
        AuthService.logout()
        document.location.reload();
    }

    render() {
        const { currentUser } = this.state;
        return (
            <Box>
                <Flex
                    bg={'white'}
                    color={'gray.600'}
                    minH={'60px'}
                    py={{ base: 2 }}
                    px={{ base: 4 }}
                    borderBottom={1}
                    borderStyle={'solid'}
                    borderColor={'gray.200'}
                    align={'center'}>
                    <Flex
                        flex={{ base: 1, md: 'auto' }}
                        ml={{ base: -2 }}
                        display={{ base: 'flex', md: 'none' }}>
                        <IconButton
                            icon={
                                <CloseIcon w={3} h={3} />
                            }
                            variant={'ghost'}
                            aria-label={'Toggle Navigation'}
                        />
                    </Flex>
                    <Flex flex={{ base: 1 }} justify={{ base: 'center', md: 'start' }}>
                        <RouteLink to ='/homepage'>
                            <Text
                                textAlign={{ base: 'center', md: 'left' }}
                                fontFamily={'heading'}
                                color={'gray.800'}>
                                Logo
                            </Text>
                        </RouteLink>
                        <Flex display={{ base: 'none', md: 'flex' }} ml={10}>
                            {currentUser ? (
                                <DesktopNav />
                            ) :(<></>)}
                        </Flex>
                    </Flex>

                    <Stack
                        flex={{ base: 1, md: 0 }}
                        justify={'flex-end'}
                        direction={'row'}
                        spacing={6}>
                        {currentUser ?  (
                            <Button
                                display={{ base: 'none', md: 'inline-flex' }}
                                fontSize={'sm'}
                                fontWeight={600}
                                color={'black'}
                                bg={'gray.400'}
                                href={'/login'}
                                _hover={{
                                    bg: 'red.100',
                                }}
                                onClick={this.logOut}>
                                <RouteLink to='/homepage'>
                                    Выход
                                </RouteLink>
                            </Button>
                        ) : <>
                            <Button
                                display={{ base: 'none', md: 'inline-flex' }}
                                fontSize={'sm'}
                                fontWeight={600}
                                color={'black'}
                                bg={'gray.400'}
                                href={'/login'}
                                _hover={{
                                    bg: 'red.100',
                                }}>
                                <RouteLink to='/register'>
                                    Регистрация
                                </RouteLink>
                            </Button>
                            <Button
                                display={{ base: 'none', md: 'inline-flex' }}
                                fontSize={'sm'}
                                fontWeight={600}
                                color={'black'}
                                bg={'gray.400'}
                                _hover={{
                                    bg: 'red.100',
                                }}>
                                <RouteLink to='/login'>
                                    Вход
                                </RouteLink>
                            </Button>
                        </>
                        }

                    </Stack>
                </Flex>
            </Box>
        );
    }
}
