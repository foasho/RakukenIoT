import 'semantic-ui-css/semantic.min.css';
import { createMedia } from '@artsy/fresnel'
import React, { Component, useEffect, useState } from 'react'
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
import Prism from 'prismjs'
import 'prismjs/components/prism-javascript' // Language
import 'prismjs/themes/prism-okaidia.css' // Theme

export enum colorPallet {
    btn="#0e0e0e",
}

const { MediaContextProvider, Media } = createMedia({
  breakpoints: {
    mobile: 0,
    tablet: 768,
    computer: 1024,
  },
})

/**
 * トップに出すイメージヘッダ
 */
interface IHomepageHeading {
    mobile: boolean;
}
const HomepageHeading = (props: IHomepageHeading) => {
    return (
        <Container text>
            <Header
                as='h1'
                content='らくけんIoT'
                inverted
                style={{
                    fontSize: props.mobile ? '2em' : '4em',
                    fontWeight: 'normal',
                    marginBottom: 0,
                    marginTop: props.mobile ? '1.5em' : '3em',
                }}
            />
            <Header
                as='h2'
                content='完全なオープンソースIoTプロジェクト'
                inverted
                style={{
                    fontSize: props.mobile ? '1.5em' : '1.7em',
                    fontWeight: 'normal',
                    marginTop: props.mobile ? '0.5em' : '1.5em',
            }}
            />
            
            <Button primary size='huge'>
                <a href='#whats' style={{color: colorPallet.btn}}>らくけんIoTとは？</a>
                <Icon name={"arrow right"} />
            </Button>
            <Button olive size='huge'>
                <a href='#usage' style={{color: colorPallet.btn}}>さっそく作ってみる</a>
                <Icon name={"arrow right"} />
            </Button>

        </Container>
    )
}



/* 
*  デスクトップ表示
*/
interface IDesktopContainer {
    children: JSX.Element,
}
const DesktopContainer = (props: IDesktopContainer) => {
    const [state, setState] = useState({fixed: false});

    const hideFixedMenu = () => setState({ fixed: false })
    const showFixedMenu = () => setState({ fixed: true })

    const { children } = props;
    const { fixed } = state;

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
                style={{ minHeight: 700, padding: '1em 0em' }}
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
                    <Menu.Item as='a' active>ホーム</Menu.Item>
                    <Menu.Item as='a'><a href='/docs'>APIリファレンス</a></Menu.Item>
                    <Menu.Item as='a'><a href='https://github.com/foasho/RakukenIoT'>Github</a></Menu.Item>
                    <Menu.Item position='right'>
                        <Button as='a' inverted={!fixed} onClick={() => window.location.href = "/login"}>
                            ログイン
                        </Button>
                        <Button as='a' inverted={!fixed} primary={fixed} style={{ marginLeft: '0.5em' }} onClick={() => window.location.href = "/signin"}>
                            作成
                        </Button>
                    </Menu.Item>
                </Container>
                </Menu>
                <HomepageHeading mobile={false} />
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
    children: JSX.Element
  }
const MobileContainer = (props: IMobileContainer) => {
    const [state, setState] = useState({sidebarOpened: false});

    const handleSidebarHide = () => setState({ sidebarOpened: false })

    const handleToggle = () => setState({ sidebarOpened: true })

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
                <Menu.Item as='a' active>ホーム</Menu.Item>
                <Menu.Item as='a'><a href='/docs'>APIリファレンス</a></Menu.Item>
                <Menu.Item as='a'><a href='https://github.com/foasho/RakukenIoT'>Github</a></Menu.Item>
                <Menu.Item as='a'>Log in</Menu.Item>
                <Menu.Item as='a'>Sign Up</Menu.Item>
            </Sidebar>

            <Sidebar.Pusher dimmed={state.sidebarOpened}>
                <Segment
                inverted
                textAlign='center'
                style={{ minHeight: 350, padding: '1em 0em' }}
                vertical
                >
                <Container>
                    <Menu inverted pointing secondary size='large'>
                    <Menu.Item onClick={handleToggle}>
                        <Icon name='sidebar' />
                    </Menu.Item>
                    <Menu.Item position='right'>
                        <Button as='a' inverted>
                        Log in
                        </Button>
                        <Button as='a' inverted style={{ marginLeft: '0.5em' }}>
                        Sign Up
                        </Button>
                    </Menu.Item>
                    </Menu>
                </Container>
                <HomepageHeading mobile />
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
interface IResponsiveContainer {
    children: JSX.Element;
  }
const ResponsiveContainer = (props: IResponsiveContainer) => (
    <MediaContextProvider>
        <DesktopContainer>{props.children}</DesktopContainer>
        <MobileContainer>{props.children}</MobileContainer>
    </MediaContextProvider>
)


/**
 * HOMEコンポネント
 * @returns 
 */
export const HomeComponent = () => {
    const [state, setState] = useState({ isMatRead: false, isBrushRead: false });
    useEffect(() => {
        Prism.highlightAll()
    }, [])
    return (
        <ResponsiveContainer>
            <>
                <Segment style={{ padding: '0em' }} vertical id="whats">
                    <Grid celled='internally' columns='equal' stackable>
                        <Grid.Row textAlign='center'>
                            <Grid.Column style={{ paddingBottom: '5em', paddingTop: '5em' }}>
                                <Header as='h3' style={{ fontSize: '2em' }}>
                                らくけんIoTとは
                                </Header>
                                <Header as='h4' style={{ fontSize: '1.5em' }}>
                                    日本語で<span style={{color: "orange", fontWeight: "bold"}}><u>らくらく健康</u></span>を略したもの
                                </Header>
                                <p style={{ fontSize: '1.33em', margin: "0 30px" , textAlign: "left"}}>
                                    自作IoTデバイスを利用して日々の健康管理を行います。
                                    <br/>
                                    <br/>
                                    本プロジェクトは、すべてオープンソースに公開したIoTプロジェクトです。
                                    このサービスページを含めてハードウェア設計とAPI/Androidネイティブソースコードすべて公開しています。
                                    <br/>
                                    開発に利用するソフトなどもすべてOSSで作られています。
                                    <br/>
                                    <br/>
                                    これを参考にし、本サービスを利用または、
                                    IoTプロジェクトのアイデアのきっかけにしてもらえると幸いです。
                                </p>
                            </Grid.Column>
                            <Grid.Column style={{ paddingBottom: '5em', paddingTop: '5em' }}>
                                <Header as='h3' style={{ fontSize: '2em' }}>
                                    システム構成
                                </Header>
                                <img src="archtecture.jfif" className="ui fluid image"/>
                            </Grid.Column>
                        </Grid.Row>
                    </Grid>
                </Segment>

                <Segment style={{ padding: '8em 0em' }} vertical id="usage">
                    <Grid container stackable verticalAlign='middle'>
                        <Grid.Row>
                            <Grid.Column width={6}>
                                <Header as='h3' style={{ fontSize: '2em' }}>
                                    デモ動画
                                </Header>
                                <Embed
                                    id='O6Xo21L0ybE'
                                    placeholder='/images/image-16by9.png'
                                    source='youtube'
                                />
                            </Grid.Column>
                            <Grid.Column floated='right' width={8}>
                                <Header as='h3' style={{ fontSize: '2em' }}>
                                    自身でサービスをホスティング
                                </Header>
                                <Header as='h3' style={{ fontSize: '1.5em' }}>
                                    事前準備
                                </Header>
                                <List bulleted>
                                    <List.Item>Pythonのインストール: バージョン3.7</List.Item>
                                    <List.Item>NodeJSのインストール: バージョン16</List.Item>
                                    <List.Item>AndroidStudioのインストール: 2021.3.1 Patch 1</List.Item>
                                </List>
                                <p style={{ fontSize: '1.33em' }}>
                                    <span>フロントエンドのビルド</span>
                                    <pre>
                                        <code className="command-line language-bash">
                                            git clone https://github.com/foasho/RakukenIoT.git
                                        </code>
                                        <br/>
                                        <code className="command-line language-bash">
                                            cd frontend
                                        </code>
                                        <br/>
                                        <code className="command-line language-bash">
                                            npm install
                                        </code>
                                        <br/>
                                        <code className="command-line language-bash">
                                            npm build
                                        </code>
                                    </pre>
                                </p>
                            </Grid.Column>
                        </Grid.Row>
                    </Grid>
                </Segment>

                <Segment style={{ padding: '8em 0em' }} vertical>
                    <Container text>
                        <Header as='h5' style={{ fontSize: '0.3em' }}>
                            サービス1
                        </Header>
                        <Header as='h3' style={{ fontSize: '2em' }}>
                            <ruby>Rakuken Mat<rt>らくけん　まっと</rt></ruby>
                        </Header>
                        <p style={{ fontSize: '1.33em' }}>
                            お風呂上りに利用する珪藻土バスマットの背面に重さセンサを取付け、
                            お風呂上りに自動で体重を測定し、測定データをグラフなどで変化を閲覧し、
                            食べ過ぎ防止などの健康管理を自動化します。
                        </p>
                        <Button as='a' size='large' onClick={() => setState({...state, isMatRead: !state.isMatRead})}>
                            もっと詳しく
                        </Button>

                        {state.isMatRead &&
                        <>
                            <Divider
                                as='h4'
                                className='header'
                                horizontal
                                style={{ margin: '3em 0em', textTransform: 'uppercase' }}
                            >
                                <a>概要</a>
                            </Divider>
                            <Header as='h3' style={{ fontSize: '1.6em' }}>
                                日々の体重管理、面倒ではありませんか?
                            </Header>
                            <img src="mat_service.jfif" className="ui fluid image"/>
                            <Divider
                                as='h4'
                                className='header'
                                horizontal
                                style={{ margin: '3em 0em', textTransform: 'uppercase' }}
                            >
                                <a>仕様</a>
                            </Divider>
                            <img src="apis.JPG" className="ui fluid image"/>
                            <img src="hardware.JPG" className="ui fluid image"/>
                            <img src="mat-app-design.JPG" className="ui fluid image"/>
                            <Divider
                                as='h4'
                                className='header'
                                horizontal
                                style={{ margin: '3em 0em', textTransform: 'uppercase' }}
                            >
                                <a>3Dビュー</a>
                            </Divider>
                            <div>
                            </div>
                            <Divider
                                as='h4'
                                className='header'
                                horizontal
                                style={{ margin: '3em 0em', textTransform: 'uppercase' }}
                            >
                                <a>ひとこと</a>
                            </Divider>
                            <p style={{ fontSize: '1.2em' }}>
                                面倒に感じるすべての部分に、IoT化できるチャンスがあります。
                                今回は、毎日体重計に乗るという健康管理と、
                                お風呂に入るという日常に組み込むことでIoTによる自動化を考えました。
                                各種設計資料および3Dモデルなどすべて公開しています。
                            </p>
                        </>
                        }
                        
                    </Container>
                </Segment>

                <Segment style={{ padding: '8em 0em' }} vertical>
                    <Container text>
                        <Header as='h5' style={{ fontSize: '0.3em' }}>
                            サービス2
                        </Header>
                        <Header as='h3' style={{ fontSize: '2em' }}>
                            <ruby>Rakuken ToothBrush<rt>らくけん歯ブラシ</rt></ruby>
                        </Header>
                        <p style={{ fontSize: '1.33em' }}>
                            毎日の日課を忘れてずに歯を磨けているかどうか、
                            普段利用している歯ブラシにセットすることで、
                            日々歯ブラシが稼働しているかを管理し、忘れたときには
                            アラートで教えてくれます。
                        </p>
                        <Button as='a' size='large' onClick={() => setState({...state, isBrushRead: !state.isBrushRead})}>
                            もっと詳しく
                        </Button>

                        {state.isBrushRead &&
                        <>
                            <Divider
                                as='h4'
                                className='header'
                                horizontal
                                style={{ margin: '3em 0em', textTransform: 'uppercase' }}
                            >
                                <a>概要</a>
                            </Divider>
                            <Header as='h3' style={{ fontSize: '1.6em' }}>
                                ...制作中...
                            </Header>
                        </>
                        }
                        
                    </Container>
                </Segment>

                <Segment inverted vertical style={{ padding: '5em 0em' }}>
                    <Container>
                        <Grid divided inverted stackable>
                        <Grid.Row>
                            <Grid.Column width={3}>
                            <Header inverted as='h4' content='About' />
                            <List link inverted>
                                <List.Item as='a' onClick={() => window.open("https://shomyapp.net/about")}>制作者</List.Item>
                                <List.Item as='a' onClick={() => window.open("https://shomyapp.net/contact")}>お問い合わせ</List.Item>
                            </List>
                            </Grid.Column>
                            <Grid.Column width={3}>
                            <Header inverted as='h4' content='Services' />
                            <List link inverted>
                                <List.Item as='a'>APIドキュメント</List.Item>
                                <List.Item as='a'>Github</List.Item>
                            </List>
                            </Grid.Column>
                            <Grid.Column width={7}>
                            <Header as='h4' inverted>
                                Design By ShoOsaka
                            </Header>
                            <p>
                                本プロジェクトは自由にご活用ください。
                                <br/>
                                また、本プロジェクト関することおよび2次的に制作されたプロジェクトに関しても、
                                一切の責任を負いかねますのでご了承の上ご活用ください。
                            </p>
                            </Grid.Column>
                        </Grid.Row>
                        </Grid>
                    </Container>
                </Segment>
            </>
        </ResponsiveContainer>
    )
}