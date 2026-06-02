class CloudGovernance < Formula
  desc "BlueArch Governance Hub"
  homepage "https://bluearch.io"
  url "https://dist.bluearch.io/cloud-governance/v0.2.1/cloud-governance_macos_arm64"
  version "v0.2.1"
  sha256 "47a96cd965b6d9a2ebb732199f862b8dadcc70a5351a1d81a467fadf73738b69"
  license :cannot_represent

  depends_on arch: :arm64
  depends_on "bluearch-core"

  def install
    bin.install "cloud-governance_macos_arm64" => "cloud-governance"
  end

  def caveats
    <<~EOS
      Governance Hub has been installed.

      Start BlueArch Core to launch installed dashboards:
        bluearch-core start --daemon
    EOS
  end

  test do
    system "#{bin}/cloud-governance", "--version"
  end
end
