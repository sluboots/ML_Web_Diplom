import {
    Flex,
    Box,
    FormControl,
    FormLabel,
    Input,
    Checkbox,
    Stack,
    Link,
    Button,
    Heading,
    Text,
    useColorModeValue,
} from '@chakra-ui/react';

import React, { Component } from "react";
import Form from "react-validation/build/form";
import {Input as input} from "react-validation/build/input";
import CheckButton from "react-validation/build/button";
import AuthService from "../../services/auth.service";


const required = value => {
    if (!value) {
        return (
            <div className="alert alert-danger" role="alert">
                This field is required!
            </div>
        );
    }
};


export default class Login extends Component {
    constructor(props) {
        super(props);
        this.handleLogin = this.handleLogin.bind(this);
        this.onChangeUsername = this.onChangeUsername.bind(this);
        this.onChangePassword = this.onChangePassword.bind(this);
        this.state = {
            username: "",
            password: "",
            loading: false,
            message: ""
        };
    }
    onChangeUsername(e) {
        this.setState({
            username: e.target.value
        });
    }
    onChangePassword(e) {
        this.setState({
            password: e.target.value
        });
    }
  handleLogin(e) {
        e.preventDefault();
        this.setState({
            message: "",
            loading: true
        });
        this.form.validateAll();
        if (this.checkBtn.context._errors.length === 0) {
            AuthService.login(this.state.username, this.state.password).then(
                () => {
                    document.location.reload();
                    window.location.assign('/homepage')
                    console.log('login access');
                },
                error => {
                    const resMessage =
                        (error.response &&
                            error.response.data &&
                            error.response.data.message) ||
                        error.message ||
                        error.toString();
                    this.setState({
                        loading: false,
                        message: resMessage
                    });
                }
            );
        } else {
            this.setState({
                loading: false
            });
        }
    }
    render(){
        return (
            <Flex
                minH={'75vh'}
                align={'center'}
                justify={'center'}
                bg={'gray.50'}>
                <Stack spacing={8} mx={'auto'} maxW={'lg'} py={12} px={6}>
                    <Stack align={'center'}  color={'gray.600'}>
                        <Heading fontSize={'4xl'}>Вход в ваш аккаунт</Heading>
                    </Stack>
                    <Form
                        onSubmit={this.handleLogin}
                        className = "form auth__form"
                        ref={c => {
                            this.form = c;
                        }}>
                        <Box
                            rounded={'lg'}
                            bg={'white'}
                            boxShadow={'lg'}
                            p={8}>
                            <Stack spacing={4}>
                                <FormControl id="email" color={'gray.600'}>
                                    <FormLabel>Имя пользователя</FormLabel>
                                    <Input type="text"
                                           className="input input--text"
                                           id="formInput#text"
                                           name="username"
                                           value={this.state.username}
                                           onChange={this.onChangeUsername}
                                           validations={[required]}/>
                                </FormControl>
                                <FormControl id="password" color={'gray.600'}>
                                    <FormLabel>Пароль</FormLabel>
                                    <Input type="password"
                                           className="input input--password"
                                           id="formInput#password"
                                           name="password"
                                           value={this.state.password}
                                           onChange={this.onChangePassword}
                                           validations={[required]} />
                                </FormControl>
                                <Stack spacing={10}>
                                    <Stack
                                        direction={{ base: 'column', sm: 'row' }}
                                        align={'start'}
                                        justify={'space-between'}>
                                        <Checkbox color={'gray.600'}>Запомнить?</Checkbox>
                                    </Stack>
                                    <Button
                                        bg={'blue.400'}
                                        color={'black'}
                                        _hover={{
                                            bg: 'blue.500',
                                        }}
                                        type="submit"
                                        disabled={this.state.loading}>
                                        Вход

                                    </Button>
                                </Stack>
                                {this.state.message && (
                                    <div className="form-group">
                                        <div className="alert alert-danger" role="alert">
                                            {this.state.message}
                                        </div>
                                    </div>
                                )}
                                <CheckButton
                                    style={{ display: "none" }}
                                    ref={c => {
                                        this.checkBtn = c;
                                    }}
                                />
                            </Stack>
                        </Box>
                    </Form>
                </Stack>
            </Flex>
        );
    }
}
