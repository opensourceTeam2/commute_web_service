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

import {
  Button,
  Card,
  CardBody,
  Container,
  Row,
  Col,
  Form,
  FormGroup,
  Label,
  Input,
} from "reactstrap";

import DemoNavbar from "components/Navbars/DemoNavbar.js";
import SimpleFooter from "components/Footers/SimpleFooter.js";

class Settings extends React.Component {
  constructor(props) {
    super(props);

    const loginId = localStorage.getItem("loginId") || "guest";
    const settingsKey = `commuteSettings_${loginId}`;
    const savedSettings = JSON.parse(localStorage.getItem(settingsKey)) || {};

    const parsedTime = this.parseSavedClassStartTime(savedSettings);

    this.state = {
      busStop: savedSettings.busStop || "",
      busNumber: savedSettings.busNumber || "",
      classStartPeriod: parsedTime.period,
      classStartClock: parsedTime.clock,
      message: "",
    };
  }

  parseSavedClassStartTime = (savedSettings) => {
    if (savedSettings.classStartPeriod && savedSettings.classStartClock) {
      return {
        period: savedSettings.classStartPeriod,
        clock: savedSettings.classStartClock,
      };
    }

    if (savedSettings.classStartTime) {
      const parts = savedSettings.classStartTime.split(" ");

      if (parts.length === 2) {
        return {
          period: parts[0],
          clock: parts[1],
        };
      }

      return {
        period: "오전",
        clock: savedSettings.classStartTime,
      };
    }

    return {
      period: "오전",
      clock: "",
    };
  };

  getTimeOptions = () => {
    const times = [];

    for (let hour = 1; hour <= 12; hour++) {
      const paddedHour = String(hour).padStart(2, "0");

      times.push(`${paddedHour}:00`);
      times.push(`${paddedHour}:30`);
    }

    return times;
  };

  componentDidMount() {
    document.documentElement.scrollTop = 0;
    document.scrollingElement.scrollTop = 0;
    this.refs.main.scrollTop = 0;
  }

  handleSave = (event) => {
    event.preventDefault();

    if (
      this.state.busStop.trim() === "" ||
      this.state.busNumber.trim() === "" ||
      this.state.classStartPeriod.trim() === "" ||
      this.state.classStartClock.trim() === ""
    ) {
      this.setState({
        message: "정류장, 버스 번호, 수업 시작 시간을 모두 입력해주세요.",
      });
      return;
    }

    const loginId = localStorage.getItem("loginId") || "guest";
    const settingsKey = `commuteSettings_${loginId}`;

    const classStartTime = `${this.state.classStartPeriod} ${this.state.classStartClock}`;

    const settings = {
      busStop: this.state.busStop,
      busNumber: this.state.busNumber,
      classStartPeriod: this.state.classStartPeriod,
      classStartClock: this.state.classStartClock,
      classStartTime: classStartTime,
    };

    localStorage.setItem(settingsKey, JSON.stringify(settings));

    this.setState({
      message: "설정이 저장되었습니다.",
    });
  };

  render() {
    const timeOptions = this.getTimeOptions();

    return (
      <>
        <DemoNavbar />

        <main className="profile-page" ref="main">
          <section className="section-profile-cover section-shaped my-0">
            <div className="shape shape-style-1 shape-default alpha-4">
              <span />
              <span />
              <span />
              <span />
              <span />
              <span />
              <span />
            </div>

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

          <section className="section">
            <Container>
              <Card className="card-profile shadow mt--300">
                <div className="px-4">
                  <Row className="justify-content-center">
                    <Col className="order-lg-2" lg="8">
                      <div className="text-center mt-5">
                        <h3>통학 설정</h3>
                        <p className="text-muted">
                          통학 도우미 실행에 사용할 기본 정보를 입력하세요.
                        </p>
                      </div>

                      <CardBody>
                        <Form onSubmit={this.handleSave}>
                          <FormGroup>
                            <Label>버스 정류장</Label>
                            <Input
                              type="text"
                              placeholder="예: 죽전역.단국대입구"
                              value={this.state.busStop}
                              onChange={(e) =>
                                this.setState({ busStop: e.target.value })
                              }
                            />
                          </FormGroup>

                          <FormGroup>
                            <Label>버스 번호</Label>
                            <Input
                              type="text"
                              placeholder="예: 720-3"
                              value={this.state.busNumber}
                              onChange={(e) =>
                                this.setState({ busNumber: e.target.value })
                              }
                            />
                          </FormGroup>

                          <FormGroup>
                            <Label>수업 시작 시간</Label>

                            <Row>
                              <Col md="4" className="mb-2">
                                <Input
                                  type="select"
                                  value={this.state.classStartPeriod}
                                  onChange={(e) =>
                                    this.setState({
                                      classStartPeriod: e.target.value,
                                    })
                                  }
                                >
                                  <option value="오전">오전</option>
                                  <option value="오후">오후</option>
                                </Input>
                              </Col>

                              <Col md="8" className="mb-2">
                                <Input
                                  type="select"
                                  value={this.state.classStartClock}
                                  onChange={(e) =>
                                    this.setState({
                                      classStartClock: e.target.value,
                                    })
                                  }
                                >
                                  <option value="">시간을 선택하세요</option>

                                  {timeOptions.map((time) => (
                                    <option key={time} value={time}>
                                      {time}
                                    </option>
                                  ))}
                                </Input>
                              </Col>
                            </Row>
                          </FormGroup>

                          {this.state.message && (
                            <p className="text-primary mt-3">
                              {this.state.message}
                            </p>
                          )}

                          <Button color="primary" type="submit">
                            저장하기
                          </Button>
                        </Form>
                      </CardBody>
                    </Col>
                  </Row>
                </div>
              </Card>
            </Container>
          </section>
        </main>

        <SimpleFooter />
      </>
    );
  }
}

export default Settings;