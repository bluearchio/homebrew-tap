class BluearchAwsTags < Formula
  desc "AWS tagging, lifecycle, tag policy, and FinOps CLI"
  homepage "https://github.com/bluearchio/bluearch-aws-tags"
  url "https://dist.bluearch.io/releases/bluearch-aws-tags/v0.12.3/tag-manager-macos-arm64.zip"
  version "v0.12.3"
  sha256 "99c43c618de197e3a58b9068f082b6a8a550700c3117c4c4c196fdb510af4e18"
  license "MIT"

  depends_on arch: :arm64
  depends_on "bluearch-aws-core"

  def install
    bin.install "tag-manager"
    alias_path = bin/"bluearch-aws-tags"
    alias_path.write <<~SH
      #!/bin/sh
      exec "#{bin}/tag-manager" "$@"
    SH
    alias_path.chmod 0755
  end

  def post_install
    # Clean up curl-installed binary to avoid PATH conflicts
    # The curl installer puts the binary at ~/.local/bin/tag-manager
    curl_binary = Pathname.new(Dir.home) / ".local" / "bin" / "tag-manager"
    if curl_binary.exist?
      begin
        ohai "Removing old curl-installed binary at #{curl_binary}"
        curl_binary.unlink
        ohai "[OK] Old binary removed successfully"
      rescue Errno::EACCES
        opoo "Permission denied: Cannot remove #{curl_binary}"
        opoo "Run manually: rm ~/.local/bin/tag-manager"
      rescue Errno::EBUSY
        opoo "File is in use: #{curl_binary}"
        opoo "Close any running tag-manager processes, then run: rm ~/.local/bin/tag-manager"
      rescue => e
        opoo "Could not remove #{curl_binary}: #{e.message}"
        opoo "Run manually: rm ~/.local/bin/tag-manager"
      end
    end
  end

  def caveats
    <<~EOS
      bluearch-aws-tags has been installed.

      Start Core first:
        bluearch-aws-core start --daemon

      Commands:
        bluearch-aws-tags --help
        tag-manager --help

      Getting started:
        bluearch-aws-tags setup validate

      Configure AWS credentials:
        export AWS_PROFILE=your-profile
        aws sso login

      Data is stored in: ~/.tag-manager/
    EOS
  end

  test do
    system "#{bin}/bluearch-aws-tags", "--version"
    system "#{bin}/tag-manager", "--version"
  end
end
