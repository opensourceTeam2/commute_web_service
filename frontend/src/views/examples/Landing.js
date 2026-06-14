/*!

=========================================================
* Argon Design System React - v1.1.2
=========================================================

* Product Page: https://www.creative-tim.com/product/argon-design-system-react
* Copyright 2023 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/argon-design-system-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import React from "react";
import { Link } from "react-router-dom";

import {
  Button,
  Card,
  CardBody,
  Container,
  Row,
  Col,
} from "reactstrap";

import DemoNavbar from "components/Navbars/DemoNavbar.js";
import CardsFooter from "components/Footers/CardsFooter.js";

class Landing extends React.Component {
  state = {
    weatherAirInfo: null,
    weatherAirLoading: true,
  };

  componentDidMount() {
    document.documentElement.scrollTop = 0;
    document.scrollingElement.scrollTop = 0;
    this.refs.main.scrollTop = 0;
    this.fetchWeatherAirInfo();
  }

  fetchWeatherAirInfo = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/main/weather-air");
      const data = await response.json();

      this.setState({
        weatherAirInfo: data,
        weatherAirLoading: false,
      });
    } catch (error) {
      this.setState({
        weatherAirInfo: null,
        weatherAirLoading: false,
      });
    }
  };

  render() {
    const { weatherAirInfo, weatherAirLoading } = this.state;

    const weather =
      weatherAirInfo && weatherAirInfo.weather
        ? weatherAirInfo.weather
        : {};

    const air =
      weatherAirInfo && weatherAirInfo.air
        ? weatherAirInfo.air
        : {};

    const rainPercent = weather.rain_percent || 0;
    const rainType = weather.rain_type || "없음";

    const weatherIcon =
      rainType === "비" || rainType === "비/눈"
        ? "☔"
        : rainType === "눈"
        ? "❄️"
        : rainPercent >= 30
        ? "🌦️"
        : "☀️";

    const airStatusMap = {
      good: "좋음",
      normal: "보통",
      bad: "나쁨",
      very_bad: "매우 나쁨",
      unknown: "정보 없음",
    };

    const airStatus = airStatusMap[air.status] || "정보 없음";

    const airIcon =
      air.status === "bad" || air.status === "very_bad"
        ? "😷"
        : air.status === "normal"
        ? "🌫️"
        : air.status === "good"
        ? "🌿"
        : "❔";
    
    const mainWeatherMessage =
      rainType === "없음" && rainPercent < 30 && air.status === "good"
        ? "오늘은 날씨도 좋고 대기질도 좋네요! 수업 끝나고 산책 어떠세요?"
        : rainType === "눈"
        ? "눈 예보가 있어요. 길이 미끄러울 수 있으니 조심해서 이동하세요."
        : rainType === "비" || rainType === "비/눈" || rainPercent >= 60
        ? "비 소식이 있어요. 이동할 때 우산을 챙기면 좋겠어요."
        : air.status === "bad" || air.status === "very_bad"
        ? "대기질이 좋지 않아요. 마스크를 챙기고 오래 걷는 건 피하는 게 좋아요."
        : rainPercent >= 30
        ? "날씨가 조금 애매해요. 혹시 모르니 작은 우산을 챙겨보세요."
        : "오늘 통학하기 무난한 날이에요. 여유 있게 출발해보세요!";

    return (
      <>
        <DemoNavbar />

        <main ref="main">
          <div className="position-relative">
            <section className="section section-lg section-shaped pb-250">
              <div className="shape shape-style-1 shape-default">
                <span />
                <span />
                <span />
                <span />
                <span />
                <span />
                <span />
                <span />
                <span />
              </div>

              <Container className="py-lg-md d-flex">
                <div className="col px-0">
                  <Row>
                    <Col lg="7">
                      <h1 className="display-3 text-white">
                        통학 시간을 예측하고
                        <span>지각 확률을 확인하세요</span>
                      </h1>

                      <Card className="shadow border-0 mt-4 mb-4">
                        <CardBody className="py-4">
                          <h6 className="text-uppercase text-muted mb-3">
                            오늘 통학 날씨 안내
                          </h6>

                          {weatherAirLoading ? (
                            <p className="mb-0 text-muted">
                              날씨와 대기질 정보를 불러오는 중입니다.
                            </p>
                          ) : (
                            <>
                              <Row>
                                <Col sm="6" className="mb-3 mb-sm-0">
                                  <div className="d-flex align-items-center">
                                    <div
                                      className="rounded-circle bg-info text-white d-flex align-items-center justify-content-center mr-3"
                                      style={{
                                        width: "48px",
                                        height: "48px",
                                        fontSize: "24px",
                                      }}
                                    >
                                      {weatherIcon}
                                    </div>
                                    <div>
                                      <h6 className="mb-1">오늘 날씨</h6>
                                      <p className="mb-0 text-muted">
                                        강수확률 {rainPercent}% · {rainType}
                                      </p>
                                    </div>
                                  </div>
                                </Col>

                                <Col sm="6">
                                  <div className="d-flex align-items-center">
                                    <div
                                      className="rounded-circle bg-success text-white d-flex align-items-center justify-content-center mr-3"
                                      style={{
                                        width: "48px",
                                        height: "48px",
                                        fontSize: "24px",
                                      }}
                                    >
                                      {airIcon}
                                    </div>
                                    <div>
                                      <h6 className="mb-1">오늘 대기질</h6>
                                      <p className="mb-0 text-muted">
                                        미세먼지 {airStatus}
                                        {air.pm10 ? ` · PM10 ${air.pm10}` : ""}
                                      </p>
                                    </div>
                                  </div>
                                </Col>
                              </Row>

                              <p className="mt-3 mb-0 text-muted">
                                {mainWeatherMessage}
                              </p>
                            </>
                          )}

                        </CardBody>
                      </Card>

                      <div className="btn-wrapper">
                        <Button
                          className="btn-icon mb-3 mb-sm-0"
                          color="info"
                          tag={Link}
                          to="/commute"
                        >
                          <span className="btn-inner--icon mr-1">
                            <i className="ni ni-bus-front-12" />
                          </span>
                          <span className="btn-inner--text">
                            통학 도우미 실행하기
                          </span>
                        </Button>

                        <Button
                          className="btn-white btn-icon mb-3 mb-sm-0 ml-1"
                          color="default"
                          tag={Link}
                          to="/settings"
                        >
                          <span className="btn-inner--icon mr-1">
                            <i className="ni ni-settings-gear-65" />
                          </span>
                          <span className="btn-inner--text">설정하기</span>
                        </Button>
                      </div>
                    </Col>
                  </Row>
                </div>
              </Container>

              <div className="separator separator-bottom separator-skew">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  preserveAspectRatio="none"
                  version="1.1"
                  viewBox="0 0 2560 100"
                  x="0"
                  y="0"
                >
                  <polygon
                    className="fill-white"
                    points="2560 0 2560 100 0 100"
                  />
                </svg>
              </div>
            </section>
          </div>

          <section className="section">
            <Container>
              <Row className="justify-content-center text-center mb-lg">
                <Col lg="8">
                  <h2 className="display-3">서비스 이용 흐름</h2>
                  <p className="lead text-muted">
                    로그인 후 설정을 입력하고, 통학 도우미 실행 화면에서 결과를
                    조회하면 됩니다.
                  </p>
                </Col>
              </Row>

              <Row>
                <Col md="4">
                  <Card className="shadow border-0 mb-4">
                    <CardBody>
                      <h5>1. 로그인</h5>
                      <p className="mb-0">
                        아이디와 비밀번호를 입력하여 서비스를 이용합니다.
                      </p>
                    </CardBody>
                  </Card>
                </Col>

                <Col md="4">
                  <Card className="shadow border-0 mb-4">
                    <CardBody>
                      <h5>2. 설정 입력</h5>
                      <p className="mb-0">
                        자주 이용하는 정류장, 버스 번호, 수업 시작 시간을
                        저장합니다.
                      </p>
                    </CardBody>
                  </Card>
                </Col>

                <Col md="4">
                  <Card className="shadow border-0 mb-4">
                    <CardBody>
                      <h5>3. 결과 조회</h5>
                      <p className="mb-0">
                        도착 예정 시간과 지각 확률을 확인하고 로그로 저장합니다.
                      </p>
                    </CardBody>
                  </Card>
                </Col>
              </Row>
            </Container>
          </section>
        </main>

        <CardsFooter />
      </>
    );
  }
}

export default Landing;