# firewall-allow

Create Inbound Rule can only allow Korea IP address in Windows Firewall

방화벽의 인바운드 규칙에 한국의 IP 주소만 허용하는 규칙을 추가하고 관리해줍니다.

- 한국 IP 주소 목록은 [한국인터넷정보센터(KRNIC)](https://xn--3e0bx5euxnjje69i70af08bea817g.xn--3e0b707e/jsp/statboard/IPAS/inter/sec/currentV4Addr.jsp)에서 가져오고 `korean_ip.txt`에 저장합니다.

- 규칙 생성 시, 포트는 RDP 포트번호인 8839로 추가되며 이는 사용자가 직접 변경해야합니다.

- 추가된 규칙은 `config.ini`에 저장되며, 규칙 업데이트 시에 해당 파일을 참고합니다.

- **중요!** 해당 프로그램은 powershell 명령어를 사용하여 방화벽 규칙을 추가하므로 powershell이 꼭 필요하며 powershell 경로가 환경변수에 등록되어 있어야 합니다.

- 아이콘 출처: [Lumicons](https://www.deviantart.com/vantler/art/Lumicons-662277185) by [vantier](https://www.deviantart.com/vantler) / [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ko)