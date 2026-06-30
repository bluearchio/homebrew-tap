class BluearchAwsGovernance < Formula
  desc "AWS Governance Hub with bundled misconfiguration catalog"
  homepage "https://github.com/bluearchio/bluearch-aws-governance"
  url "https://github.com/bluearchio/bluearch-aws-governance/releases/download/v0.2.2/cloud-governance_macos_arm64"
  version "v0.2.2"
  sha256 "79cf0c2c0a7ea3740f6b52f80cec39d8a7c30d7ae057e3472ee80e7232e54a01"
  license :cannot_represent

  depends_on arch: :arm64
  depends_on "bluearch-aws-core"

  def install
    bin.install "cloud-governance_macos_arm64" => "cloud-governance"
  end

  def caveats
    <<~EOS
      bluearch-aws-governance has been installed.

      Start BlueArch Core to launch installed dashboards:
        bluearch-core start --daemon
    EOS
  end

  test do
    system "#{bin}/cloud-governance", "--version"
  end
end
