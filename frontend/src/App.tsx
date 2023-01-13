import React, { Component, useEffect, useState } from 'react'
import { Route, BrowserRouter, Routes } from "react-router-dom"
import 'semantic-ui-css/semantic.min.css';
import { createMedia } from '@artsy/fresnel'
import {
    Button,
    Container,
    Divider,
    Embed,
    Grid,
    Header,
    Icon,
    Image,
    List,
    Menu,
    Segment,
    Sidebar,
    Visibility,
} from 'semantic-ui-react';
import styles from "./App.module.scss";
import { HomeComponent } from './components/pages/Home/Home';
import { LoginComponent } from './components/pages/Login/Login';
import { SignUpComponent } from './components/pages/SignUp/SignUp';

/**
 * ページ一覧
 *  /:home
 *  /:docs
 *  /:github
 *  /:login
 *  /:signup
 *  /:userpage/{:user_id}
 */

export enum colorPallet {
  btn="#0e0e0e",
}

export const { MediaContextProvider, Media } = createMedia({
breakpoints: {
  mobile: 0,
  tablet: 768,
  computer: 1024,
},
})

/**
 * トップに出すイメージヘッダ
 */
export interface IHomepageHeading {
    mobile: boolean;
}
export const HomepageHeading = (props: IHomepageHeading) => {
  return (
      <Container text>
          <Header
              as='h1'
              inverted
              style={{
                  fontSize: props.mobile ? '2em' : '3.3em',
                  marginBottom: 0,
                  marginTop: props.mobile ? '1.5em' : '3em',
              }}
          >
              <span><ruby>らくけん<rt style={{fontSize: "0.3em"}}>らくらく健康管理</rt></ruby>-IoT</span>
          </Header>
          <Header
              as='h2'
              content='完全なオープンソースIoTプロジェクト'
              inverted
              style={{
                  fontSize: props.mobile ? '1.5em' : '1.7em',
                  fontWeight: 'normal',
                  marginTop: props.mobile ? '0.5em' : '1.5em',
                  marginLeft: "1em",
                  marginRight: "1em",
          }}
          />
          <Header
              as='h3'
              content='IoTハードウェア・連携API・ネイティブアプリ・Webアプリのすべてをオープンソースで公開'
              inverted
              style={{
                  fontSize: props.mobile ? '1.5em' : '1.7em',
                  fontWeight: 'normal',
                  marginTop: props.mobile ? '0.5em' : '1.5em',
                  marginBottom: props.mobile ? '1.0em' : '1.5em',
                  marginLeft: "1em",
                  marginRight: "1em",
          }}
          />
          <div style={{ display: props.mobile ? "block": "inline-block", marginBottom: props.mobile ? "0.6em": "0" }}>
              <a href='#whats'>
                  <Button size='huge' style={{background: "#FFFFFF"}}>
                      らくけんIoTとは？
                      <Icon name={"arrow right"} />
                  </Button>
              </a>
          </div>
          <div style={{ display: props.mobile ? "block": "inline-block", marginBottom: props.mobile ? "0.6em": "0" }}>
              <a href='#usage' style={{color: colorPallet.btn}}>
                  <Button olive size='huge' style={{background: "#27666A", color: "#FFFFFF"}}>
                      さっそく作ってみる
                      <Icon name={"arrow right"} />
                  </Button>
              </a>
          </div>

      </Container>
  )
}

/* 
*  デスクトップ表示
*/
export interface IDesktopContainer {
    children: JSX.Element,
    isHeading: boolean;
}
export const DesktopContainer = (props: IDesktopContainer) => {
    const [state, setState] = useState({fixed: false});

    const hideFixedMenu = () => setState({ fixed: false })
    const showFixedMenu = () => setState({ fixed: true })

    const { children } = props;
    const { fixed } = state;

    const routing = window.location.pathname;

    return (
        <Media greaterThan='mobile'>
            <Visibility
                once={false}
                onBottomPassed={showFixedMenu}
                onBottomPassedReverse={hideFixedMenu}
            >
                <Segment
                    inverted
                    textAlign='center'
                    style={{ background: "linear-gradient(180deg, #38D4DE 0%, #75C6CB 50%, #ECFEFF 100%)", minHeight: 700, padding: '1em 1em' }}
                    vertical
                >
                    <Menu
                        fixed={fixed ? 'top' : undefined}
                        inverted={!fixed}
                        pointing={!fixed}
                        secondary={!fixed}
                        size='large'
                    >
                    <Container>
                        <Menu.Item as='a' active={routing=="/"? true: false} onClick={() => window.location.href = "/"}>ホーム</Menu.Item>
                        <Menu.Item as='a'><a href='/docs'>APIリファレンス</a></Menu.Item>
                        <Menu.Item as='a'><a href='https://github.com/foasho/RakukenIoT'>Github</a></Menu.Item>
                        <Menu.Item position='right'>
                            <Button as='a' inverted={!fixed} onClick={() => window.location.href = "/login"}>
                                ログイン
                            </Button>
                            <Button as='a' inverted={!fixed} primary={fixed} style={{ marginLeft: '0.5em' }} onClick={() => window.location.href = "/signup"}>
                                アカウント作成
                            </Button>
                        </Menu.Item>
                    </Container>
                    </Menu>
                    {props.isHeading &&
                        <HomepageHeading mobile={false} />
                    }
                </Segment>
            </Visibility>

            {children}
        </Media>
    )
}


/**
* モバイル表示
*/
interface IMobileContainer {
  children: JSX.Element;
  isHeading: boolean;
}
export const MobileContainer = (props: IMobileContainer) => {
    const [state, setState] = useState({sidebarOpened: false});

    const handleSidebarHide = () => setState({ sidebarOpened: false })

    const handleToggle = () => setState({ sidebarOpened: true })

    const routing = window.location.pathname;

    return (
        <Media at='mobile'>
            <Sidebar.Pushable>
            <Sidebar
                as={Menu}
                animation='overlay'
                inverted
                onHide={handleSidebarHide}
                vertical
                visible={state.sidebarOpened}
            >
                <Menu.Item as='a' active={routing=="/"? true: false} onClick={() => window.location.href = "/"}>ホーム</Menu.Item>
                <Menu.Item as='a'><a href='/docs'>APIリファレンス</a></Menu.Item>
                <Menu.Item as='a'><a href='https://github.com/foasho/RakukenIoT'>Github</a></Menu.Item>
                <Menu.Item as='a' active={routing=="/login"? true: false} onClick={() => window.location.href = "/login"}>ログイン</Menu.Item>
                <Menu.Item as='a' active={routing=="/signup"? true: false} onClick={() => window.location.href = "/signup"}>アカウント作成</Menu.Item>
            </Sidebar>

            <Sidebar.Pusher dimmed={state.sidebarOpened}>
                <Segment
                inverted
                textAlign='center'
                style={{  background: "linear-gradient(180deg, #38D4DE 0%, #75C6CB 50%, #ECFEFF 100%)", minHeight: 350, padding: '1em 0em' }}
                vertical
                >
                    <Container>
                        <Menu inverted pointing secondary size='large'>
                        <Menu.Item onClick={handleToggle}>
                            <Icon name='sidebar' />
                        </Menu.Item>
                        <Menu.Item position='right'>
                            <Button as='a' inverted>
                            ログイン
                            </Button>
                            <Button as='a' inverted style={{ marginLeft: '0.5em' }}>
                            アカウント作成
                            </Button>
                        </Menu.Item>
                        </Menu>
                    </Container>
                    {props.isHeading &&
                        <HomepageHeading mobile={true} />
                    }
                </Segment>
                {props.children}
            </Sidebar.Pusher>
            </Sidebar.Pushable>
        </Media>
    )
}

/**
 * Responsiveコンポーネント
 */
export interface IResponsiveContainer {
  children: JSX.Element;
  isHeading: boolean;
}
export const ResponsiveContainer = (props: IResponsiveContainer) => (
  <MediaContextProvider>
      <DesktopContainer isHeading={props.isHeading}>{props.children}</DesktopContainer>
      <MobileContainer isHeading={props.isHeading}>{props.children}</MobileContainer>
  </MediaContextProvider>
)

export const App = () => {


    return (
        <div className={styles.appMain}>
        <BrowserRouter>
            <Routes>
                <Route path='/' element={
                    <ResponsiveContainer isHeading={true}>
                        <HomeComponent/>
                    </ResponsiveContainer>
                }></Route>

                <Route path='/login' element={
                    <ResponsiveContainer isHeading={false}>
                        <LoginComponent/>
                    </ResponsiveContainer>
                }></Route>

                <Route path='/signup' element={
                    <ResponsiveContainer isHeading={false}>
                        <SignUpComponent/>
                    </ResponsiveContainer>
                }></Route>

                <Route path='/userpage/{:user_id}' element={
                    <HomeComponent/>
                    }></Route>
            </Routes>
        </BrowserRouter>
        </div>
    );
}