import React, {
  useEffect,
  useState
} from "react";

import {
  Container,
  Row,
  Col,
  Card,
  CardBody
} from "reactstrap";

import easyColor from "assets/img/badges/easy_color.png";
import easyGray from "assets/img/badges/easy_gray.png";

import hardColor from "assets/img/badges/hard_color.png";
import hardGray from "assets/img/badges/hard_gray.png";

import rainColor from "assets/img/badges/rain_color.png";
import rainGray from "assets/img/badges/rain_gray.png";

import morningColor from "assets/img/badges/morning_color.png";
import morningGray from "assets/img/badges/morning_gray.png";

import strongColor from "assets/img/badges/strong_color.png";
import strongGray from "assets/img/badges/strong_gray.png";

import DemoNavbar from "components/Navbars/DemoNavbar.js";
import CardsFooter from "components/Footers/CardsFooter.js";

export default function Badge() {

  const [badgeData, setBadgeData] =
    useState(null);

  const [theme, setTheme] =
    useState(
      localStorage.getItem(
        "selectedTheme"
      ) || "default"
    );

    const [semester, setSemester] =
      useState("");

  useEffect(() => {

    const loginId =
      localStorage.getItem(
        "loginId"
      );

    fetch(
      `http://127.0.0.1:8000/badge?login_id=${loginId}`
    )
      .then((response) =>
        response.json()
      )
      .then((data) => {
        setBadgeData(data);
      });

    fetch(
      "http://127.0.0.1:8000/semester"
    )
      .then((response) =>
        response.json()
      )
      .then((data) => {
        setSemester(
          data.semester
        );
      });
  
  }, []);

  useEffect(() => {

    const loginId =
      localStorage.getItem(
        "loginId"
      );

    fetch(
      `http://127.0.0.1:8000/themes?login_id=${loginId}`
    )
      .then((response) =>
        response.json()
      )
      .then((data) => {
        setTheme(
          data?.selected_theme ||
          "default"
        );
      })
      .catch(() => {
        setTheme(
          "default"
        );
      });

  }, []);

  return (
    <>
      <DemoNavbar />

    <main>
      <section className="section section-shaped section-lg">
        <div
          className="shape shape-style-1"
          style={{
            background:
              theme === "pink"
                ? "linear-gradient(150deg,#ffb6c1 15%,#ff8fab 70%,#ff5e8a 94%)"
                : theme === "purple"
                ? "linear-gradient(150deg,#c8a2ff 15%,#a66cff 70%,#8b4dff 94%)"
                : theme === "blue"
                ? "linear-gradient(150deg,#7795f8 15%,#6772e5 70%,#555abf 94%)"
                : "linear-gradient(150deg,#172b4d 15%,#1a174d 70%,#22204d 94%)"
          }}
        >
          <span />
          <span />
          <span />
          <span />
          <span />
          <span />
          <span />
          <span />
        </div>
          <Container className="pt-lg-7">
            <Row className="justify-content-center">
              <Col lg="10">
                <Card className="shadow border-0">
                <CardBody className="p-5">
                  <Row>
                    <Col md="6">
                      <h3 className="font-weight-bold">
                        🏆 포인트 / 뱃지
                      </h3>
                      <p
                        className="text-muted"
                        style={{
                          fontSize: "16px",
                          marginBottom: "0px"
                        }}
                      >
                        ※ 포인트와 뱃지는 학기 종료 시 초기화됩니다.
                      </p>
                    </Col>
                    <Col
                      md="6"
                      className="text-right"
                    >
                      <p
                        className="text-muted"
                        style={{
                          marginTop: "5px"
                        }}
                      >
                        현재 학기: {semester}
                      </p>
                    </Col>
                  </Row>
                  <h5 className="mt-4">
                    총 포인트: {badgeData?.total_points || 0}P
                  </h5>
                  <h5 className="mt-2">
                    획득 뱃지: {badgeData?.badge_count || 0} / 5
                  </h5>
                  <Row className="mt-5 justify-content-center">
                    <Col md="4" className="text-center mb-4">
                      <p className="mt-2 text-muted">
                        {badgeData?.easy_success_count || 0} / 30
                      </p>
                      <img
                        src={
                          badgeData?.badge_list?.includes("여유로운 통학의 신")
                          ? easyColor
                          : easyGray
                        }
                        alt=""
                        style={{
                            width: "180px",
                            height: "180px",
                            objectFit: "contain"
                        }}
                      />
                    </Col>
                    <Col md="4" className="text-center mb-4">
                      <p className="mt-2 text-muted">
                        {badgeData?.hard_success_count || 0} / 10
                      </p>
                      <img
                        src={
                          badgeData?.badge_list?.includes("아슬아슬 마스터")
                          ? hardColor
                          : hardGray
                        }
                        alt=""
                        style={{
                            width: "180px",
                            height: "180px",
                            objectFit: "contain"
                        }}
                      />
                    </Col>
                </Row>
                    <Row className="justify-content-center">
                    <Col md="4" className="text-center mb-4">
                      <p className="mt-2 text-muted">
                        {badgeData?.rain_success_count || 0} / 10
                      </p>
                      <img
                        src={
                          badgeData?.badge_list?.includes("비를 뚫는 자")
                          ? rainColor
                          : rainGray
                        }
                        alt=""
                        style={{
                            width: "180px",
                            height: "180px",
                            objectFit: "contain"
                        }}
                      />
                    </Col>
                    <Col md="4" className="text-center mb-4">
                      <p className="mt-2 text-muted">
                        {badgeData?.early_morning_count || 0} / 20
                      </p>
                      <img
                        src={
                          badgeData?.badge_list?.includes("새벽 통학생")
                          ? morningColor
                          : morningGray
                        }
                        alt=""
                        style={{
                            width: "180px",
                            height: "180px",
                            objectFit: "contain"
                        }}
                      />
                    </Col>
                    <Col md="4" className="text-center mb-4">
                      <p className="mt-2 text-muted">
                        {badgeData?.long_distance_count || 0} / 20
                      </p>
                      <img
                        src={
                          badgeData?.badge_list?.includes("강철 체력")
                          ? strongColor
                          : strongGray
                        }
                        alt=""
                        style={{
                            width: "180px",
                            height: "180px",
                            objectFit: "contain"
                        }}
                      />
                    </Col>
                  </Row>
                </CardBody>
              </Card>
            </Col>
          </Row>
          <Card className="mt-5 shadow border-0">
            <CardBody>
              <Row>
                {/* 왼쪽 */}
                <Col md="6">
                  <h3 className="mb-4">
                  📖 포인트 도감
                  </h3>
                  <ul>
                    <li>
                      <strong>
                        여유로운 통학 성공
                      </strong>
                      <br />
                      지각 확률 20% 이하 통학 성공
                      (+40P)
                    </li>
                    <br />
                    <li>
                      <strong>
                        아슬아슬 통학 성공
                      </strong>
                      <br />
                      지각 확률 50% 이상 통학 성공
                      (+20P)
                   </li>
                    <br />
                   <li>
                      <strong>
                        험난한 날씨 속 통학 성공
                      </strong>
                     <br />
                      비 / 눈 오는 날 통학 성공
                      (+10P)
                   </li>
                    <br />
                    <li>
                     <strong>
                       혼잡 시간 통학 성공
                     </strong>
                     <br />
                     출퇴근 시간 통학 성공
                     (+10P)
                   </li>
                  </ul>
                </Col>

                {/* 오른쪽 */}
                <Col md="6">
                 <h3 className="mb-4">
                  📖 뱃지 도감
                  </h3>
                  <ul>
                    <li>
                      <strong>
                        여유로운 통학의 신
                      </strong>
                      <br />
                      지각 확률 20% 이하 30회 성공
                    </li>
                    <br />
                    <li>
                      <strong>
                        아슬아슬 마스터
                      </strong>
                      <br />
                      지각 확률 50% 이상 10회 성공
                    </li>
                    <br />
                    <li>
                      <strong>
                        비를 뚫는 자
                      </strong>
                      <br />
                      비 / 눈 오는 날 10회 성공
                    </li>
                    <br />
                    <li>
                      <strong>
                        새벽 통학생
                      </strong>
                      <br />
                      오전 7시 이전 통학 20회 성공
                    </li>
                    <br />
                    <li>
                      <strong>
                        강철 체력
                      </strong>
                      <br />
                      편도 1시간 이상 통학 20회 성공
                    </li>
                  </ul>
                  <p className="mt-4 text-muted">
                    * 뱃지 획득 시 추가 +50P 지급
                  </p>
                </Col>
              </Row>
            </CardBody>
          </Card>
        </Container>
      </section>
    </main>
    <CardsFooter />
  </>
);
}